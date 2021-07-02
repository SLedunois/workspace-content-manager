import requests
import json
import dateutil
import logging

class Workspace:
    def __init__(self):
        self.server = 'http://127.0.0.1:3000'
        pass

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
        path: string
            Resource path
        """
        url = '{}/directories?path={}'.format(self.server, path)
        r = requests.get(url)
        return r.json()

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

    def get_notebook(self, path='', content=True):
        """
        Get from remote workspace

        Parameters
        ----------
        type: string
            Resource type. Can be directory of file

        path: string
            Resource path
        """
        return self.get_file(path, content)

    def file_exists(self, path):
        """
        Check if file exists. It returns True if file exists, otherwise returns False

        Parameters
        ----------
        path: string
            Path file to check
        """
        url = '{}/files/exists?path={}'.format(self.server, path)
        r = requests.get(url)
        if r.status_code == 404:
            return False
        elif r.status_code == 409:
            return True

        logging.error('Response status neither `Not found` nor `Conflict`: {}'.format(r.status_code))
        return True

    def directory_exists(self, path):
        """
        Check if directory exists. If exists it returns True, otherwise it returns False

        Parameters
        ----------
        path: string
            Path folder to check.
        """
        url = '{}/directories/exists?path={}'.format(self.server, path)
        r = requests.get(url)
        if r.status_code == 404:
            return False
        elif r.status_code == 409:
            return True

        logging.error('Response status neither `Not found` nor `Conflict`: {}'.format(r.status_code))
        return True

    def save(self, path, model):
        """
        Save item. Based on model type, it save a folder or an item. It returns saved model

        Parameters
        ----------
        path: string
            Object path to save

        model: json
            New model value to save
        """
        logging.error('Into workspace save method for path {} and model {}'.format(path, model))
        if model['type'] == 'directory':
            logging.error('Item to save is a directory')
            return self._save_directory(path)
        else:
            logging.error('Item to save is not a directory')
            return self._save_item(path, model)

    def _save_directory(self, path):
        """
        Save directory

        Parameters
        ---------
        path: string
            Directory path to save
        """
        logging.error("Saving directory for path {}".format(path))
        url = '{}/directories?path={}'.format(self.server, path)
        r = requests.post(url)
        folder = r.json()
        folder['content'] = None
        folder['format'] = None
        return folder

    def _save_item(self, path, model):
        """
        Save item. It can be a file or  a notebook. If item already exists, update it.

        Parameters
        ----------
        path: string
            Path item to update

        model: json
            New object
        """
        url = '{}/files?path={}'.format(self.server, path)
        r = None
        if self.file_exists(path):
            r = requests.put(url, json=model)
        else:
            r = requests.post(url, json=model)
        item = r.json()
        item['content'] = None
        item['format'] = None
        return item

    def is_type(self, path, type):
        """
        Check path type

        Parameters
        ---------
        path: string
            Item path to check

        type: string
            Type to check. It can be `notebook`, `folder` or `file`
        """
        url = '{}/type?path={}&type={}'.format(self.server, path, type)
        r = requests.get(url)
        return r.status_code == 200

    def rename(self, old_path, new_path):
        """
        Rename old_path to new_path

        Parameters
        ---------
        old_path: string
            Old path that need a rename

        new_path: string
            Old path gonna be rename to new path
        """
        logging.error('Renaming {} to {}'.format(old_path, new_path))
        url = '{}/files/rename?old_path={}&new_path={}'.format(self.server, old_path, new_path)
        r = requests.put(url)
        logging.error('Request status code = {}'.format(r.status_code))
        logging.error('Rename content is {}'.format(json.dumps(r.json())))

        #Here content should be None
        item = r.json()
        item['Content'] = None

        return item

