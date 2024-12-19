import sys
import logging
from webgme_bindings import PluginBase


# Setup a logger
logger = logging.getLogger('ansiblePlayStep')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
class ansiblePlayStep(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node
        # Log the name of the active node
        name = core.get_attribute(active_node, 'name')
        logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))
        # Commit any changes to the model in WebGME
        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        logger.info('Committed: {0}'.format(commit_info))
        # Call the function to generate the step play content
        self.children=self.core.load_children(self.active_node)
        self.generate_play()
        # Indicate that the plugin has executed successfully
        self.result_set_success(True)
        
    

    def get_task_content(self, task_node):
        
        task_content = f"  - name: {self.core.get_attribute(task_node, 'name')}\n"
        # Retrieve attributes related to the task and add them as task properties
        attribute_names = self.core.get_attribute_names(task_node)
        for attribute in attribute_names:
            if attribute != "name":  # Skip the 'name' attribute (already used as task name)
                value = self.core.get_attribute(task_node, attribute)
                task_content += f"    {attribute}: {value}\n"
        return task_content
    def get_objs_of_meta(self, metatype):
        
        _names_, _nodes_ = [], []
        for child in self.core.load_children(self.active_node):
            if self.core.is_type_of(child, self.META[metatype]):
                _names_.append(self.core.get_attribute(child, 'name'))
                _nodes_.append(child)
        return _names_, _nodes_
    def get_objs_of_meta_in_parent(self, parent_node, metatype):
       
        _names_, _nodes_ = [], []
        for child in self.core.load_children(parent_node):
            if self.core.is_type_of(child, self.META[metatype]):
                _names_.append(self.core.get_attribute(child, 'name'))
                _nodes_.append(child)
        return _names_, _nodes_
    def get_objs_of_meta_in_children(self, children_node, metatype):
       
        _names_, _nodes_ = [], []
        for child in self.core.load_children(children_node):
            if self.core.is_type_of(child, self.META[metatype]):
                _names_.append(self.core.get_attribute(child, 'name'))
                _nodes_.append(child)
        return _names_, _nodes_
    
    def get_connection_info(self, connection_nodes):
        
        src_dst = []
        for connection in connection_nodes:
            _src_ = self.core.load_pointer(connection, 'src')
            _dst_ = self.core.load_pointer(connection, 'dst')
            src_dst.append([_src_, _dst_])
        return src_dst
    # def generate_step_play(self):
    # # Retrieve the first 'play' node, assuming there's only one
    #     play_names, play_nodes = self.get_objs_of_meta('play')
    
    #     if not play_nodes:
    #         logger.warning("No 'play' nodes found!")
    #         return
    
    # # Use the first play node only
    #     play_node = play_nodes[0]
    #     play_name = play_names[0]
    
    # # Initialize the play content as a string
    #     play_content = f"- name: {play_name}\n  hosts: all\n"
    
    # # Get all attributes of the play node
    #     attribute_names = self.core.get_attribute_names(play_node)
    
    #     for attribute in attribute_names:
    #     # Handle the 'collections' attribute separately
    #         if attribute == "collections":
    #             play_content += "  collections:\n"
    #             collections = self.core.get_attribute(play_node, attribute).split('\n')
    #             for collection in collections:
    #                 play_content += f"    - {collection}\n"
    #     # Handle other attributes except 'name' and 'file'
    #         elif attribute not in {"name", "file"}:
    #             play_content += f"  {attribute}: {self.core.get_attribute(play_node, attribute)}\n"
    
    # # Add tasks section
    #     play_content += "  tasks:\n"
    # # Retrieve the tasks inside the play node
    #     task_names, task_nodes = self.get_objs_of_meta_in_parent(play_node, 'task')
    
    #     for task_name, task_node in zip(task_names, task_nodes):
    #         play_content += self.get_task_content(task_node)
    
    # # Save the generated play content as a YAML file
    #     output_filename = self.get_current_config().get("file_name", "playbook_step_master")
    #     self.add_file(f"{output_filename}.yaml", play_content)
    #     logger.info("Generated Step Play YAML content:\n" + play_content)


#    def playbook_generate(self):
#         # Get all the nodes of type 'Playbook'
#         play_names,play_nodes=self.get_objs_of_meta('play')
#         for play_name,play_node in zip(play_names,play_nodes):
#             attribute_names=self.core.get_attribute_names(play_node)
#             self.playbook_string+=f"- name: {self.core.get_attribute(play_node,'name')}\n"
#             for attribute in attribute_names:
                
#                 if attribute=="collections":
#                     self.playbook_string+=f"  collections:\n"
#                     collections=self.core.get_attribute(play_node,attribute).split('\n')
#                     for collection in collections:
#                         self.playbook_string+=f"    - {collection}\n"
#                 elif attribute!="name" and attribute!="file":
#                     self.playbook_string+=f"  {attribute}: {self.core.get_attribute(play_node,attribute)}\n"

    def generate_play(self):
        play_names, play_nodes = self.get_objs_of_meta('play')
        play_node = play_nodes[0]
        play_name = play_names[0]
        print("Inside the generate play")
        print(play_names)
        print(play_nodes)
        self.play_content=f"- name: {play_name}\n"
        # self.local=self.core.get_attribute(play_nodes[0],'hosts')
        for a,node in enumerate(play_nodes):
            self.play_content+=f"  hosts: {self.core.get_attribute(node,'hosts')}\n"
            self.play_content+=f"  remote_user: {self.core.get_attribute(node,'remote_user')}\n"
            self.play_content+=f"  gather_facts: {self.core.get_attribute(node,'gather_facts')}\n"
            self.play_content+=f"  become: {self.core.get_attribute(node,'become')}\n"
            attribute_names=self.core.get_attribute_names(node)
            for attribute in attribute_names:

                if(attribute=='collections'):
                    print("Inside collections")
                    self.play_content+=f"  collections:\n"
                    collections=self.core.get_attribute(node,'collections').split('\n')
                    for collection in collections:
                        self.play_content+=f"    - {collection}\n"
                
                

            self.play_content+=f"  tasks:\n"
            for child_playbook in self.core.load_children(node):
                self.play_content+=f"  - import_tasks: {self.core.get_attribute(child_playbook,'name')}\n" 
        # attribute=self.get_objs_of_meta_in_parent(play_nodes,'play')
        print(self.play_content)
        # print("Children")
        # print('attribute',attribute_names)
        # print(attribute)