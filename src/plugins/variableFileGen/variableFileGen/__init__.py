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
        self.k8s_info_generate()
        self.cloud_info_generate()
        self.docker_info_generate()
        self.helms_info_generate()
        self.ovs_info_generate()
        self.kafka_info_generate()

        self.vars_string+=self.ubuntu_info_string
        self.vars_string+=self.k8s_info_string
        self.vars_string+=self.cloud_info_string
        self.vars_string+=self.docker_info_string
        self.vars_string+=self.helms_info_string
        self.vars_string+=self.ovs_info_string
        self.vars_string+=self.kafka_info_string

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
                if name!='name':
                    self.ubuntu_info_string+=f"    {name}: {self.core.get_attribute(node,name)}\n"

        
        print(self.ubuntu_info_string)

    def k8s_info_generate(self):
        self.k8s_info_string = ''
        k8s_names,k8s_nodes=self.get_objs_of_meta('K8s')
        self.k8s_info_string +="K8s:\n"
        for node in k8s_nodes:
            # print("attributes of k8s", self.core.get_attribute_names(node))
            attribute_names=self.core.get_attribute_names(node)
            for name in attribute_names:

                if name=="teams":
                    self.k8s_info_string+=f"    {name}:\n"
                    # print("teams: ",self.core.get_attribute(node,name))
                    team_info=self.core.get_attribute(node,name).split('\n')
                    for team in team_info:
                        self.k8s_info_string+=f"        - {team}\n"
                    # self.k8s_info_string+=f"        - {self.core.get_attribute(node,'name')}\n"

                elif name!='name':
                    self.k8s_info_string+=f"    {name}: {self.core.get_attribute(node,name)}\n"
    
    def cloud_info_generate(self):
        self.cloud_info_string = ''
        cloud_names,cloud_nodes=self.get_objs_of_meta('cloud')
        self.cloud_info_string +="cloud:\n"
        for node in cloud_nodes:
            # print("attributes of cloud", self.core.get_attribute_names(node))
            attribute_names=self.core.get_attribute_names(node)
            for name in attribute_names:

                if name == "bastion_security_groups" or name =="vm_security_groups":
                    print("name: ",name)
                    self.cloud_info_string+=f"    {name}:\n"
                    security_info=self.core.get_attribute(node,name).split('\n')
                    for info in security_info:
                        self.cloud_info_string+=f"        - {info}\n"

                elif name!='name':
                    self.cloud_info_string+=f"    {name}: {self.core.get_attribute(node,name)}\n"

    def docker_info_generate(self):
        self.docker_info_string = ''
        docker_names,docker_nodes=self.get_objs_of_meta('Docker')
        self.docker_info_string +="docker:\n"
        for node in docker_nodes:
            # print("attributes of docker", self.core.get_attribute_names(node))
            attribute_names=self.core.get_attribute_names(node)
            for name in attribute_names:
                if name!='name':
                    self.docker_info_string+=f"    {name}: {self.core.get_attribute(node,name)}\n"
    
    def helms_info_generate(self):
        self.helms_info_string = ''
        helms_names,helms_nodes=self.get_objs_of_meta('helm')
        self.helms_info_string +="helm:\n"
        for node in helms_nodes:
            # print("attributes of helm", self.core.get_attribute_names(node))
            attribute_names=self.core.get_attribute_names(node)
            for name in attribute_names:
                if name!='name':
                    self.helms_info_string+=f"    {name}: {self.core.get_attribute(node,name)}\n"

    def ovs_info_generate(self):
        self.ovs_info_string = ''
        ovs_names,ovs_nodes=self.get_objs_of_meta('ovs')
        self.ovs_info_string +="ovs:\n"
        for node in ovs_nodes:
            # print("attributes of ovs", self.core.get_attribute_names(node))
            attribute_names=self.core.get_attribute_names(node)
            for name in attribute_names:
                if name!='name':
                    self.ovs_info_string+=f"    {name}: {self.core.get_attribute(node,name)}\n"
    
    def kafka_info_generate(self):
        self.kafka_info_string = ''
        kafka_names,kafka_nodes=self.get_objs_of_meta('kafka')
        self.kafka_info_string +="kafka:\n"
        for node in kafka_nodes:
            # print("attributes of kafka", self.core.get_attribute_names(node))
            attribute_names=self.core.get_attribute_names(node)
            for name in attribute_names:
                if name!='name':
                    self.kafka_info_string+=f"    {name}: {self.core.get_attribute(node,name)}\n"





