import requests
import json
import dateutil


class Workspace:
    def __init__(self):
        pass

    def _base_model(self, path, resource):
        """Build the common base of a contents model
        Parameters
        ----------
        path: string
            The path to the resource
        resource: json
            The file or folder model
        """
        date = 'Sat Oct 11 17:13:46 UTC 2003'
        return {
            'name': resource['name'],
            'path': path,
            'content': None,
            'format': None,
            'mimetype': None,
            'writable': True,
            'created': dateutil.parser.parse(date),
            'last_modified': dateutil.parser.parse(date),
            'type': None
        }

    def _file_model(self, path, file, content=True, format=None):
        """Build a model for a file
        if content is requested, include the file contents
        """
        model = self._base_model(path, file)
        model['type'] = 'file'
        model['mimetype'] = file['mimetype']
        model['path'] = '/' + file['name']
        if content:
            model['content'] = file['content']

        return model

    def _dir_model(self, path, resource, content=True, format=None):
        """Build a model for a directory
        if content is requested, will include a listing of the directory
        """
        model = self._base_model(path, resource)
        model['type'] = 'directory'
        if content:
            model['content'] = contents = []
            for content in resource['content']:
                contents.append(self._file_model(path, content, False))
            model['content'] = contents

        model['format'] = 'json'

        return model

    @staticmethod
    def _txt_file(path):
        date = 'Sat Oct 11 17:13:46 UTC 2003'
        return {
            'content': 'Hello world',
            'created': dateutil.parser.parse(date),
            'last_modified': dateutil.parser.parse(date),
            'format': 'json',
            'mimetype': 'text/plain',
            'path': path,
            'name': path.replace('/', ''),
            'writable': True
        }

    def getDirectory(self, path=''):
        """
        Get from remote workspace

        Parameters
        ----------
        type: string
            Resource type. Can be directory of file

        path: string
            Resource path
        """
        url = 'http://127.0.0.1:4010/directories'
        r = requests.get(url)
        result = self._dir_model(path, r.json())
        return result

    def getFile(self, path=''):
        """
        Get from remote workspace

        Parameters
        ----------
        type: string
            Resource type. Can be directory of file

        path: string
            Resource path
        """
        url = 'http://127.0.0.1:4010/directories/files'
        r = requests.get(url)
        result = self._file_model(path, self._txt_file(path), False)
        result['format'] = 'text'
        result['content'] = r.text
        return result


    def getNotebook(self, path=''):
        """
        Get from remote workspace

        Parameters
        ----------
        type: string
            Resource type. Can be directory of file

        path: string
            Resource path
        """
        return None
