import logging
import dateutil
import os
import json

from notebook.services.contents.manager import ContentsManager
from tornado import web

from .workspace import Workspace
from .checkpoints import WorkspaceCheckpoints


class WorkspaceContentsManager(ContentsManager):

    def __init__(self, *args, **kwargs):
        super(WorkspaceContentsManager, self).__init__(*args, **kwargs)
        self.cm = Workspace()
        self.checkpoints_class = WorkspaceCheckpoints

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
        logging.error("Looking if directory {} exists ?".format(path))
        exists = self.cm.directory_exists(path)
        logging.error("Directory {} exists ? {}".format(path, exists))
        return exists

    def is_hidden(self, path):
        """Is path a hidden directory or file?
        Parameters
        ----------
        path : string
            The path to check. This is an API path (`/` separated, relative to root dir).
        Returns
        -------
        hidden : bool
            Whether the path is hidden.

        """
        logging.error("Looking if {} is hidden".format(path))
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
        logging.error("Checking if {} file exist".format(path))
        return self.cm.file_exists(path)

    """
    # Getting base content
    [Into get manager method]
        Path =
        Content = 1
        Content is not True!
        Type = None
        Format = None
    
    # Opening file
    # This call seems to be ok. Path = file name, Type = file, Format = text
    [Into get manager method]
        Path = /ameliorated_sleek.mmf
        Content = 1
        Content is not True!
        Type = file
        Format = text
        
    # Jupyter refresh the base content
    [Into get manager method]
        Path =
        Content = 1
        Content is not True!
        Type = None
        Format = None
        
    # Jupyter tries to open file as a directory when base content describe it as file. WTF ?
    [Into get manager method]
        Path = /ameliorated_sleek.mmf
        Content = True
        Type = directory
        Format = None
    """

    def get(self, path, content=True, type='directory', format=None):
        """Get a file or directory model."""
        logging.error("Into get manager method")
        logging.error("Path = {}".format(path))
        logging.error("Content = {}".format(content))
        if content is not True or content is not 1:
            logging.error("Content is not True!")
        logging.error("Type = {}".format(type))
        logging.error("Format = {}".format(format))

        if type is 'file':
            return self.cm.get_file(path, content)

        if type is 'notebook':
            return self.cm.get_notebook(path, content)

        if type is 'directory':
            return self.cm.get_directory(path)

        # In this case. Type is none. First check the type
        types = ['directory', 'file', 'notebook']
        logging.error("Type is None. Checking type in remote")
        for type in types:
            logging.error("Checking type {} for path {}".format(type, path))
            if self.cm.is_type(path, type):
                logging.error("Path {} is of type {}".format(path, type))
                return self.get(path, content, type, format)

        raise web.HTTPError(404, '{} does not exists in any types'.format(path))

        # if type == 'file':
        #     return self.cm.get_file(path, content)
        # elif type == 'notebook' or (type is None and path.endswith('.ipynb')):
        #     return self.cm.get_notebook(path, content)
        # else:
        #     # if self.cm.directoryExists(path) is not True:
        #     #     raise web.HTTPError(404, '{} directory does not exists'.format(path))
        #     if self.cm.file_exists(path):
        #         logging.error('The {} file exists !'.format(path))
        #         return self.cm.get_file(path, content)
        #
        #     if self.cm.directory_exists(path):
        #         logging.error("Finally, it's a directory")
        #         return self.cm.get_directory(path)

    def save(self, model, path):
        """
        Save a file or directory model to path.
        Should return the saved model with no content.  Save implementations
        should call self.run_pre_save_hook(model=model, path=path) prior to
        writing any data.
        """
        logging.error("Into save method")
        logging.error("Model = {}".format(model))
        logging.error("Path = {}".format(path))
        return self.cm.save(path, model)

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
        logging.error("Trying to rename file from path {} to {}".format(old_path, new_path))
        return self.cm.rename(old_path, new_path)

    def delete(self, path):
        """Delete a file/directory and any associated checkpoints."""
        logging.error("delete")
        return None

    def rename(self, old_path, new_path):
        """Rename a file and any checkpoints associated with that file."""
        logging.error("Trying to rename from {} to {}".format(old_path, new_path))
        if self.cm.is_type(old_path, 'file'):
            return self.rename_file(old_path, new_path)

        return self.cm.rename(old_path, new_path)
