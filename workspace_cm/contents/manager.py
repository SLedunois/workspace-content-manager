import logging
import dateutil
import os
import json
from notebook.services.contents.manager import ContentsManager
from .workspace import Workspace


class WorkspaceContentsManager(ContentsManager):

    def __init__(self, *args, **kwargs):
        super(WorkspaceContentsManager, self).__init__(*args, **kwargs)
        print(os.environ["JUPYTERHUB_USER"])
        self.cm = Workspace()

    def dir_exists(self, path):
        """Does a directory exist at the given path?
        Like os.path.isdir

        Parameters
        ----------
        path : string
            The path to check
        Returns
        -------
        exists : bool
            Whether the path does indeed exist.

        """
        logging.error("dir_exists")
        logging.error("path = " + path)
        return False

    def is_hidden(self, path):
        """Is path a hidden directory or file?
        Parameters
        ----------
        path : string
            The path to check. This is an API path (`/` separated,
            relative to root dir).
        Returns
        -------
        hidden : bool
            Whether the path is hidden.

        """
        logging.error("is_hidden")
        return False

    def file_exists(self, path=''):
        """Does a file exist at the given path?
        Like os.path.isfile

        Parameters
        ----------
        path : string
            The API path of a file to check for.
        Returns
        -------
        exists : bool
            Whether the file exists.

        """
        logging.error("file_exists")
        logging.error("path = " + path)
        return False

    def get(self, path, content=True, type='directory', format=None):
        """Get a file or directory model."""
        logging.error("get")
        logging.error("Path = " + path)
        return self.cm.get(type, path)

    def save(self, model, path):
        """
        Save a file or directory model to path.
        Should return the saved model with no content.  Save implementations
        should call self.run_pre_save_hook(model=model, path=path) prior to
        writing any data.
        """
        logging.error("save")
        return None

    def delete_file(self, path, allow_non_empty=False):
        """Delete the file or directory at path."""
        logging.error("delete_file")
        return None

    def rename_file(self, old_path, new_path):
        """
        Rename a file or directory.

        N.B. Note currently we only support renaming, not moving to another folder.
        Its not clear that this operation can be performed using rename, it doesn't
        seem to be exposed through jlab.
        """
        logging.error("rename_file")
        return None

    def delete(self, path):
        """Delete a file/directory and any associated checkpoints."""
        logging.error("delete")
        return None

    def rename(self, old_path, new_path):
        """Rename a file and any checkpoints associated with that file."""
        logging.error("rename")
        return None