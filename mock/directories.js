const Files = require('./files');

const model = {
    id: '5c93abf2-3a06-4abf-b0b0-62b565eb8df3',
    name: 'base',
    path: '',
    last_modified: 'Sat Oct 11 17:13:46 UTC 2003',
    created: 'Sat Oct 11 17:13:46 UTC 2003',
    type: 'directory',
    format: 'json',
    writable: true,
    mimetype: null
}

class Directories {
    content = new Files();
    map = {};

    constructor() {
        this.data = model;
        this.data.content = this.content.files;
    }

    exists(path) {
        console.log(`Checking if ${path} folder exists`)
        console.log(Object.keys(this.map));
        if (path.trim() === '') {
            return !path || path.trim() === ''
        } else {
            console.log(`Path exists ? ${path in this.map}`)
            return path in this.map;
        }
    }

    create(path) {
        const folder = Object.assign({}, model);
        folder.path = `/${path}`;
        folder.name = path.replace('/', '');
        folder.content = [];
        console.log(path);
        this.map[path] = folder;
        this.content.putDirectory(folder.path, folder);
        return folder;
    }
}

module.exports = Directories;