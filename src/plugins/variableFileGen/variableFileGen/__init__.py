"""
This is where the implementation of the plugin code goes.
The variableFileGen-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('variableFileGen')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class variableFileGen(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node

        name = core.get_attribute(active_node, 'name')

        print("active node: ", active_node)

        logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))

        # core.set_attribute(active_node, 'name', 'newName')

        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        logger.info('committed :{0}'.format(commit_info))

        self.children=[]
        for child in self.core.load_children(self.active_node):
             self.children.append(child)
             print("child: ",core.get_attribute(child, 'name') )

        
        self.vars_string=''
        self.ubuntu_info_generate()
        self.vars_string+=self.ubuntu_info_string

        
        # self.generate_subnet_config()
        # self.generate_hosts_config()
        # self.generate_agent_config()
        
        # self.cyborg_config=''
        # self.cyborg_config+= self.agent_string
        # self.cyborg_config+=self.host_string
        # self.cyborg_config+=self.subnet_string
        

        # Return the config file
        output_filename = self.get_current_config().get("file_name")
        if not output_filename:
            output_filename = self.core.get_attribute(self.active_node, "name")
        self.add_file(f"{output_filename}.yaml", str(self.vars_string))
        self.result_set_success(True)

    def get_objs_of_meta(self,metatype):
        #return names of node and node objects of given meta type
        _names_,_nodes_=[],[]
        for child in self.children:
           if self.core.is_type_of(child,self.META[metatype]): 
               #self.get_all_attributes_values(child)
               #self.get_all_childrens(child)
               _nodes_.append(child)
               _names_.append(self.core.get_attribute(child,'name'))
        return _names_,_nodes_ 

    def ubuntu_info_generate(self):
        self.ubuntu_info_string = ''
        ubuntu_names,ubuntu_nodes=self.get_objs_of_meta('ubuntu')
        self.ubuntu_info_string +="ubuntu:\n"
        for node in ubuntu_nodes:
            # print("attributes of ubuntu", self.core.get_attribute_names(node))
            attribute_names=self.core.get_attribute_names(node)
            for name in attribute_names:
                self.ubuntu_info_string+=f"    {name}: {self.core.get_attribute(node,name)}\n"

        
        print(self.ubuntu_info_string)





