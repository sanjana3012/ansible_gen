"""
This is where the implementation of the plugin code goes.
The ansibleWorkflow-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import os
import logging
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

        children = core.load_children(active_node)
        for child in children:
            node_name = core.get_attribute(child, 'name')
            file_hash = core.get_registry(child, 'generatedFileHash')
            
            if file_hash:
                try:
                    file_content = self.get_file(file_hash)
                    
                    node_type = core.get_meta_type(child)
                    type_name = core.get_attribute(node_type, 'name')
                    extension = '.yaml'
                    if type_name == 'inventory_instance':
                        extension = '.ini'
                        
                    output_file = os.path.join(base_dir, f'{node_name}{extension}')
                    with open(output_file, 'w') as f:
                        f.write(file_content)
                    logger.info(f'Downloaded file to: {output_file}')
                    
                except Exception as e:
                    logger.error(f'Failed to process file for {node_name}: {str(e)}')

        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        logger.info('committed :{0}'.format(commit_info))
        
        self.result_set_success(True)
