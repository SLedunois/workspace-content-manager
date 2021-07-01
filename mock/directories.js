const Files = require('./files');

const data = {
    id: '5c93abf2-3a06-4abf-b0b0-62b565eb8df3',
    name: 'base',
    path: '',
    last_modified: 'Sat Oct 11 17:13:46 UTC 2003',
    created: 'Sat Oct 11 17:13:46 UTC 2003',
}

class Directories {
    content = new Files();
    map = {};

    constructor() {
        this.data = data;
        this.data.content = this.content.files;
    }

    exists(path) {
        return !path || path.trim() === ''
    }
}

module.exports = Directories;