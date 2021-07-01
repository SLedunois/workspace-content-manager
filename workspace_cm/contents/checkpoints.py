import logging
import requests
import json
from notebook.services.contents.checkpoints import Checkpoints, GenericCheckpointsMixin


class WorkspaceCheckpoints(GenericCheckpointsMixin, Checkpoints):
    """requires the following methods:"""

    def create_file_checkpoint(self, content, format, path):
        """ -> checkpoint model"""
        logging.error("Create file checkpoint for path {}".format(path))
        logging.error("Content = {}".format(content))
        logging.error("Format = {}".format(format))
        body = {
            'content': content
        }
        url = 'http://127.0.0.1:3000/files/checkpoints?path={}'.format(path)
        r = requests.post(url, json=body)
        cp = r.json()
        logging.error('Checkpoint created: {}'.format(json.dumps(cp)))
        return cp

    def create_notebook_checkpoint(self, nb, path):
        """ -> checkpoint model"""
        logging.error("Create checkpoint notebook for path {}".format(path))
        logging.error("Checkpoint notebook is {}".format(nb))

    def get_file_checkpoint(self, checkpoint_id, path):
        """ -> {'type': 'file', 'content': <str>, 'format': {'text', 'base64'}}"""
        logging.error("Get file checkpoint for checkpoint_id {}".format(checkpoint_id))
        return None

    def get_notebook_checkpoint(self, checkpoint_id, path):
        """ -> {'type': 'notebook', 'content': <output of nbformat.read>}"""
        logging.error("Get notebook for checkpoint_id {}".format(checkpoint_id))

    def delete_checkpoint(self, checkpoint_id, path):
        """deletes a checkpoint for a file"""
        logging.error("Delete checkpoint for checkpoint_id {}".format(checkpoint_id))

    def list_checkpoints(self, path):
        """
        Return a list of checkpoints for a given file.
        :param str path: The path to the file from which the checkpoint was
                         created.
        """
        logging.error("List checkpoints for path {}".format(path))
        url = 'http://127.0.0.1:3000/directories/files/checkpoints?path={}'.format(path)
        r = requests.get(url)
        return r.json()

    def rename_checkpoint(self, checkpoint_id, old_path, new_path):
        """renames checkpoint from old path to new path"""
        logging.error("Rename checkpoints for checkpoint_id {}".format(checkpoint_id))
