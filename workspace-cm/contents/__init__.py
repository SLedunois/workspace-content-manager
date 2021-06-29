from notebook.services.contents.manager import ContentsManager

class WorkspaceContentsManager(ContentsManager):

    def __init__(self, *args, **kwargs):
        super(WorkspaceContentsManager, self).__init__(*args, **kwargs)

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

        path = path.strip('/')
        girder_path = self._get_girder_path(path)

        return self._resource_exists(girder_path, ['folder', 'item', 'user'])

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

        return False

    def get(self, path, content=True, type=None, format=None):
        """Get a file or directory model."""

        return None

    def save(self, model, path):
        """
        Save a file or directory model to path.
        Should return the saved model with no content.  Save implementations
        should call self.run_pre_save_hook(model=model, path=path) prior to
        writing any data.
        """
        return None

    def delete_file(self, path, allow_non_empty=False):
        """Delete the file or directory at path."""
        return None

    def rename_file(self, old_path, new_path):
        """
        Rename a file or directory.

        N.B. Note currently we only support renaming, not moving to another folder.
        Its not clear that this operation can be performed using rename, it doesn't
        seem to be exposed through jlab.
        """
        return None

    def delete(self, path):
        """Delete a file/directory and any associated checkpoints."""
        return None

    def rename(self, old_path, new_path):
        """Rename a file and any checkpoints associated with that file."""
        return None