"""
This is where the implementation of the plugin code goes.
The inventoryFileGen-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase
import os   # for creating the inventory directory

# Setup a logger
logger = logging.getLogger('inventoryFileGen')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class inventoryFileGen(PluginBase):
    
    def main(self):
        # Setup Node --------------------------------------------------------------
        core = self.core
        root_node = self.root_node
        active_node = self.active_node

        name = core.get_attribute(active_node, 'name')
        logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))

        # -------------------------------------------------------------------

        self.inventory_string = ''  # The final string that will be written to the inventory file. Made up of the strings below
        self.local_MC_string = ''   # The string for the local machine
        self.hostnames_string = ''  # The string for the hostnames defined by the user

        self.children = self.core.load_children(self.active_node)   # Get children of inventory

        # Get inventory folder from parent of inventory node
        inventory_folder = self.core.get_parent(self.active_node)
        inventory_folder_path = self.core.get_attribute(inventory_folder, 'path')
        # Create the inventory folder if it does not exist - if writing to filesystem instead of WebGME
        #if not os.path.exists(inventory_folder_path) or not os.path.isdir(inventory_folder_path):
        #    os.mkdir(inventory_folder_path)

        # Set up the output config file (i.e. the inventory file)
        inventory_filename = self.get_current_config().get("file_name")
        if not inventory_filename:
            inventory_filename = self.core.get_attribute(self.active_node, "name")
        # inventory_file_path = inventory_folder_path + '/' + inventory_filename
        # print(inventory_file_path)

        # Construct the inventory string
        self.Local_MC_info_generate()
        self.Hostnames_info_generate()
        self.inventory_string += self.local_MC_string + '\n'
        self.inventory_string += self.hostnames_string

        # Add file and store hash
        output_filename = self.get_current_config().get("file_name")
        if not output_filename:
            output_filename = core.get_attribute(active_node, "name")
            
        file_hash = self.add_file(f"{output_filename}.ini", str(self.inventory_string))
        
        # Store hash in registry
        core.set_registry(active_node, 'generatedFileHash', file_hash)
        logger.info(f'Generated file hash: {file_hash}')

        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Generated inventory and stored hash')
        logger.info('committed :{0}'.format(commit_info))
        
        self.result_set_success(True)

    def get_objs_of_meta(self, metatype):
        # Helper function to retrieve nodes of given meta type
        names, nodes = [], []
        for child in self.children:
           if self.core.is_type_of(child, self.META[metatype]): 
               #self.get_all_attributes_values(child)
               #self.get_all_childrens(child)
               nodes.append(child)
               names.append(self.core.get_attribute(child, 'name'))
        return names, nodes 

    def Local_MC_info_generate(self):
        self.local_MC_string += '[LocalMC]\n'
        names, nodes = self.get_objs_of_meta('LocalMC')

        # Write the local machine IP
        self.local_MC_string += self.core.get_attribute(nodes[0], 'ip') + ' '

        # Write any variables for the local machine
        attributes = self.core.get_attribute_names(nodes[0])
        for attribute in attributes:
            value = self.core.get_attribute(nodes[0], attribute)
            if (value) and (attribute != 'name') and (attribute != 'ip'):
                self.local_MC_string += attribute + '=' + str(value) + '\n'

        #print(self.local_MC_string)

    def Hostnames_info_generate(self):
        names, nodes = self.get_objs_of_meta('Hostname')
        for i, node in enumerate(nodes):

            # skip base class
            if names[i] == 'Hostname':
                continue

            # Write the hostname and the IP(s) associated with it
            self.hostnames_string += '[' + self.core.get_attribute(node, 'name') + ']\n'
            self.hostnames_string += self.core.get_attribute(node, 'ips') + '\n'

            # Write the variables for the hostname
            self.hostnames_string += '\n[' + self.core.get_attribute(node, 'name') + ':vars]\n'
            attributes = self.core.get_attribute_names(node)
            for attribute in attributes:
                value = self.core.get_attribute(node, attribute)
                if (value) and (attribute != 'name') and (attribute != 'ips'):
                    self.hostnames_string += attribute + '=' + str(value) + '\n'
            self.hostnames_string += '\n'

        #print(self.hostnames_string)






        
