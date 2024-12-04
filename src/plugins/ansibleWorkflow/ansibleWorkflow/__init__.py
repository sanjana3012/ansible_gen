"""
This is where the implementation of the plugin code goes.
The ansibleWorkflow-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import os
import logging
import subprocess
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('ansibleWorkflow')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ansibleWorkflow(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node

        workflow_name = core.get_attribute(active_node, 'name')
        base_dir = f'ansible_workflows/{workflow_name}'
        os.makedirs(base_dir, exist_ok=True)

        inventory_path = None
        playbook_path = None
        vars_path = None

        children = core.load_children(active_node)
        for child in children:
            node_name = core.get_attribute(child, 'name')
            file_hash = core.get_registry(child, 'generatedFileHash')
            
            if file_hash:
                try:
                    file_content = self.get_file(file_hash)
                    
                    node_type = core.get_meta_type(child)
                    type_name = core.get_attribute(node_type, 'name')
                    
                    if type_name == 'inventory':
                        extension = '.ini'
                        output_file = os.path.join(base_dir, f'{node_name}{extension}')
                        inventory_path = output_file
                    elif type_name == 'playbook':
                        extension = '.yml'
                        output_file = os.path.join(base_dir, f'{node_name}{extension}')
                        playbook_path = output_file
                    elif type_name == 'variable_file':
                        extension = '.yml'
                        output_file = os.path.join(base_dir, f'{node_name}{extension}')
                        vars_path = output_file
                    
                    with open(output_file, 'w') as f:
                        f.write(file_content)
                    logger.info(f'Downloaded file to: {output_file}')
                    
                except Exception as e:
                    logger.error(f'Failed to process file for {node_name}: {str(e)}')
                    self.create_message(child, f'Failed to process file: {str(e)}', 'error')
                    return

        # Start ansible
    # Start ansible
        if inventory_path and playbook_path and vars_path:
            try:
                # Change to workflow directory
                os.chdir(base_dir)

                # Create ansible-playbook command
                cmd = ['ansible-playbook', '-i', os.path.basename(inventory_path)]
                cmd.extend(['-e', f'@{os.path.basename(vars_path)}'])
                cmd.append(os.path.basename(playbook_path))
                cmd.append('-vvv')  # Add verbose flag for detailed output

                logger.info(f"Current working directory: {os.getcwd()}")
                logger.info(f"Ansible command: {' '.join(cmd)}")

                # Run the ansible-playbook command
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                stdout, stderr = process.communicate()

                if process.returncode == 0:
                    logger.info('Ansible playbook executed successfully')
                    logger.info(f'STDOUT:\n{stdout}')
                    self.create_message(active_node, 'Ansible playbook executed successfully', 'info')
                else:
                    logger.error('Ansible playbook failed')
                    logger.error(f'STDERR:\n{stderr}')
                    logger.error(f'STDOUT:\n{stdout}')
                    self.create_message(active_node, f'Ansible playbook failed: {stderr}', 'error')

            except Exception as e:
                logger.error(f'Failed to execute Ansible: {str(e)}')
                self.create_message(active_node, f'Failed to execute Ansible: {str(e)}', 'error')
                return
        else:
            logger.error('Missing required files for Ansible execution')
            self.create_message(active_node, 'Missing required inventory, vars, or playbook files', 'error')
            return


        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        logger.info('committed :{0}'.format(commit_info))
        
        self.result_set_success(True)
