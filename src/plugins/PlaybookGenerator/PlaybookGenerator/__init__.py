"""
This is where the implementation of the plugin code goes.
The PlaybookGenerator-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
import os
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('PlaybookGenerator')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PlaybookGenerator(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node

        name = core.get_attribute(active_node, 'name')

        logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))

        self.children=[]
        for child in self.core.load_children(self.active_node):
             self.children.append(child)
             print("child: ",core.get_attribute(child, 'name') )
        
        self.children_of_parent=[]
        for child in self.core.load_children(self.core.get_parent(self.active_node)):
             self.children_of_parent.append(child)
             print("child of parent: ",core.get_attribute(child, 'name') )
        
        self.playbook_string=''
        self.playbook_generate()

        output_filename = self.get_current_config().get("file_name")
        if not output_filename:
            output_filename = core.get_attribute(self.active_node, "name")
            
        # Add file and get hash
        file_hash = self.add_file(f"{output_filename}.yaml", str(self.playbook_string))
        
        # Store the hash in the node's registry
        core.set_registry(active_node, 'generatedFileHash', file_hash)
        logger.info(f'Generated file hash: {file_hash}')

        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        logger.info('committed :{0}'.format(commit_info))
        
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
        
    def get_objs_of_parent_meta(self,metatype):
        _names_,_nodes_=[],[]
        for child in self.children_of_parent:
           if self.core.is_type_of(child,self.META[metatype]): 
               #self.get_all_attributes_values(child)
               #self.get_all_childrens(child)
               _nodes_.append(child)
               _names_.append(self.core.get_attribute(child,'name'))
        return _names_,_nodes_
    
    
    def get_connection_info(self,connection_nodes):
        src_dst=[]
        #print("**** still here****")
        for connection in connection_nodes: 
            #print('Connection name is:',self.core.get_attribute(connection,'name'))
            _src_= (self.core.load_pointer(connection,'src'))
            _dst_= (self.core.load_pointer(connection,'dst'))
            #print("=> Get own pointer name:",self.core.get_own_pointer_names(connection) )
            #print("=> pointer src is:",_src_ ,",dst is:",_dst_ )
            src_dst.append([_src_,_dst_])
        return src_dst
        
    
    def playbook_generate(self):
    # Initialize playbook string
        self.playbook_string = ""
        ansible_workflow_node=self.core.get_parent(self.active_node)
        if self.core.get_attribute(ansible_workflow_node,'path_to_ansible_automation_root'):
            #print("Path to Ansible Automation root found in attribute")
            tasks_path=self.core.get_attribute(ansible_workflow_node,'path_to_ansible_automation_root')+"/tasks/"
        elif not self.core.get_attribute(ansible_workflow_node,'path_to_ansible_automation_root'):
            #print("made up a path")
            tasks_path=str(os.getcwd())+"/AnsibleAutomation/tasks/"
        else:
            logger.error("Path to Ansible Automation root not found")
        
        print("tasks_path:",tasks_path)
        # Get all the nodes of type 'Playbook'
        ordered_tasks = []
        play_names, play_nodes = self.get_objs_of_meta('play')

        for play_name, play_node in zip(play_names, play_nodes):
            attribute_names = self.core.get_attribute_names(play_node)

            # Add play-level attributes to the playbook string
            self.playbook_string += f"- name: {self.core.get_attribute(play_node, 'name')}\n"
            for attribute in attribute_names:
                if attribute == "collections" and self.core.get_attribute(play_node, attribute):
                    self.playbook_string += f"  collections:\n"
                    collections = self.core.get_attribute(play_node, attribute).split('\n')
                    for collection in collections:
                        self.playbook_string += f"    - {collection}\n"
                elif attribute=="path_to_ansible_python_interpreter" and self.core.get_attribute(play_node, attribute):
                    self.playbook_string += f"  vars:\n    ansible_python_interpreter: {self.core.get_attribute(play_node, attribute)}\n"
                elif attribute != "name" and attribute != "file" and attribute != "order_of_execution" and attribute!="path_to_ansible_python_interpreter" and self.core.get_attribute(play_node, attribute):
                    self.playbook_string += f"  {attribute}: {self.core.get_attribute(play_node, attribute)}\n"


            # Add tasks section
            self.playbook_string += f"  tasks:\n"
            for child_playbook in self.core.load_children(play_node):
                order_of_execution = self.core.get_attribute(child_playbook, 'order_of_execution')
                print("Order of execution:", order_of_execution, "for node:", self.core.get_attribute(child_playbook, 'name'))
                ordered_tasks.append((child_playbook, order_of_execution))

            # Sort all tasks by order of execution after adding them
            ordered_tasks.sort(key=lambda x: x[1])
            print("Ordered tasks:", ordered_tasks)

            # Add sorted tasks to the playbook string
            for child_playbook, _ in ordered_tasks:
                self.playbook_string += f"    - import_tasks: {tasks_path}{self.core.get_attribute(child_playbook, 'name')}.yml\n"

        print(self.playbook_string)


                
            

            
