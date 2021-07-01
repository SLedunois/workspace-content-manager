import requests
import json
import dateutil
import logging

class Workspace:
    def __init__(self):
        self.server = 'http://127.0.0.1:3000'
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

    def get_directory(self, path=''):
        """
        Get from remote workspace

        Parameters
        ----------
        type: string
            Resource type. Can be directory of file

        path: string
            Resource path
        """
        url = '{}/directories?path={}'.format(self.server, path)
        r = requests.get(url)
        result = self._dir_model(path, r.json())
        return result

    def get_file(self, path='', content=True):
        """
        Get from remote workspace

        Parameters
        ----------
        path: string
            Resource path

        content: bool
            item needs content
        """
        url = '{}/directories/files?path={}'.format(self.server, path)
        r = requests.get(url)
        item = r.json()
        if content is False or content is 0:
            item['content'] = None
            item['format'] = None

        logging.error('Before returning get file value. Need content ? {} : {}'.format(content, json.dumps(item)))
        return item

    def get_notebook(self, path=''):
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

    def file_exists(self, path):
        url = '{}/files/exists?path={}'.format(self.server, path)
        r = requests.get(url)
        if r.status_code == 404:
            return False
        elif r.status_code == 409:
            return True

        logging.error('Response status neither `Not found` nor `Conflict`: {}'.format(r.status_code))
        return True

    def directory_exists(self, path):
        url = '{}/directories/exists?path={}'.format(self.server, path)
        r = requests.get(url)
        if r.status_code == 404:
            return False
        elif r.status_code == 409:
            return True

        logging.error('Response status neither `Not found` nor `Conflict`: {}'.format(r.status_code))
        return True

    def save(self, path, model):
        url = '{}/files?path={}'.format(self.server, path)
        r = requests.post(url, json=model)
        item = r.json()
        item['content'] = None
        item['format'] = None
        return item

