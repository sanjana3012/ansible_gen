"""
This is where the implementation of the plugin code goes.
The playGenerator-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase
import requests
import yaml
# Setup a logger
logger = logging.getLogger('playGenerator')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class playGenerator(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node

        name = core.get_attribute(active_node, 'name')

        logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))

        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        logger.info('committed :{0}'.format(commit_info))

        file_hash=(core.get_attribute(active_node,'file'))
        print("file content is:", (file_hash))
        

        # WebGME server details
        self.WEBGME_URL = ' http://127.0.0.1:8888'
  
        if file_hash:
            file_content = self.download_asset(file_hash)
            if file_content:
                # Convert the file content (assumed to be YAML) into a dictionary
                try:
                    file_dict = yaml.safe_load(file_content.decode('utf-8'))  # Parse YAML content
                    print(f"File as dictionary:\n{file_dict}")
                except yaml.YAMLError as exc:
                    print(f"Error parsing YAML content: {exc}")
        else:
            print("Failed to retrieve file content.")


        # Blob URL for fetching the asset
    def get_blob_url(self,file_hash):
        return f'{self.WEBGME_URL}/rest/blob/download/{file_hash}'

    def download_asset(self,file_hash):
        url = self.get_blob_url(file_hash)
        response = requests.get(url)  # No authorization headers, assuming open access

        if response.status_code == 200:
            return response.content  # The content of the file
        else:
            print(f"Error downloading asset: {response.status_code} - {response.text}")
            return None
