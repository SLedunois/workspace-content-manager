const date = date;

const data = {
    id: 'fa39326b-d215-4584-810c-346e3274ccd6',
    name: 'lorem.txt',
    path: '/lorem.txt',
    last_modified: date,
    created: date,
    content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse faucibus mauris nulla, at varius odio tempor in. Mauris nibh urna, euismod eget ante sed, consectetur accumsan elit. Vivamus scelerisque ultrices nulla, a sodales urna scelerisque in. Curabitur porttitor sodales congue. Quisque convallis tempus suscipit. Cras facilisis nisi non accumsan egestas. Donec blandit augue a ligula fermentum cursus.',
    format: 'text',
    mimetype: 'text/plain',
    writable: true,
    type: 'file'
}


const checkpoints = [
    {
        id: 'f04a4273-965a-4140-a339-c09b95aa489f',
        last_modified: date
    },
    {
        id: '85d21e60-0e33-4e34-a964-7cb8630c197c',
        last_modified: 'Sat Oct 11 18:13:46 UTC 2003'
    }
];

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

class Files {
    files = [];
    map = {};
    versions = {};

    constructor() {
        this.versions[data.path] = checkpoints;
        this.files.push(data);
        this.files.forEach(file => this.map[file.path] = file);
    }

    file(path) {
        return this.map[path];
    }

    checkpoints(path) {
        return this.versions[path];
    }

    exists(path) {
        return path in this.map;
    }

    put(path, model) {
        const { type } = model;
        model.id = uuidv4();
        model.name = path;
        model.path = `/${path}`;
        model.last_modified = date;
        model.created = date;
        model.writable = true;

        switch (type) {
            case 'file':
                model.mimetype = 'text/plain';
                break;
        }

        this.files.push(model);
        this.map[model.path] = model;

        this.versions[model.path] = checkpoints;

        console.info(JSON.stringify(model));

        return model;
    }
}

module.exports = Files;