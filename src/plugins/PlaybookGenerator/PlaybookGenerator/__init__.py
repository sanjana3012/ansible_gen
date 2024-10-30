"""
This is where the implementation of the plugin code goes.
The PlaybookGenerator-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
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

        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        logger.info('committed :{0}'.format(commit_info))

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

        # Return the config file
        output_filename = self.get_current_config().get("file_name")
        if not output_filename:
            output_filename = self.core.get_attribute(self.active_node, "name")
        self.add_file(f"{output_filename}.yaml", str(self.playbook_string))
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
        # Get all the nodes of type 'Playbook'
        play_names,play_nodes=self.get_objs_of_meta('play')
        for play_name,play_node in zip(play_names,play_nodes):
            attribute_names=self.core.get_attribute_names(play_node)
            self.playbook_string+=f"- name: {self.core.get_attribute(play_node,'name')}\n"
            for attribute in attribute_names:
                
                if attribute=="collections":
                    self.playbook_string+=f"  collections:\n"
                    collections=self.core.get_attribute(play_node,attribute).split('\n')
                    for collection in collections:
                        self.playbook_string+=f"    - {collection}\n"
                elif attribute!="name" and attribute!="file":
                    self.playbook_string+=f"  {attribute}: {self.core.get_attribute(play_node,attribute)}\n"

            # connection_nodes,connection_names=self.get_objs_of_parent_meta('connection')
            # connections=self.get_connection_info((connection_nodes))
            # print("connections are: ",connection_names)
            # for connection in connections:
            #     print("hello")
            #     if self.active_node in connection:
            #         print("hello_part_2")
            #         src_node=connection[0]
            #         dst_node=connection[1]
            #         print("src node is: ", self.core.get_attribute(src_node,"name"))
            #         print("dst node is: ", self.core.get_attribute(dst_node,"name"))
                
            self.playbook_string+=f"  tasks:\n"
            for child_playbook in self.core.load_children(play_node):
                self.playbook_string+=f"  - import_tasks: {self.core.get_attribute(child_playbook,'name')}\n" 
        print(self.playbook_string)
                
            

            
