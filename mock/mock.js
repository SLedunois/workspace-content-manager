const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

const Directories = require('./directories');
const directories = new Directories(); 7

app.use(bodyParser.json());

app.get("/directories", (req, res) => {
    let path = req.query.path;
    console.log(`Looking for directory ${path} content`);
    if (path.trim() === '') {
        res.json(directories.data);
        return;
    }

    if (!path.startsWith('/')) {
        path = `/${path}`;
    }

    if (directories.content.exists(path)) {
        res.json(directories.content.file(path));
    } else {
        console.log(`Directory content for path ${path} not found`);
        res.status(404).end();
    }
});

app.get('/directories/files', (req, res) => {
    const path = req.query.path;
    console.info(`Looking for ${path} file`);
    const file = directories.content.file(path);
    if (file) res.json(file);
    else res.status(404).end();
});

app.get('/directories/exists', (req, res) => {
    const path = req.query.path;
    console.info(`Checking if ${path} directory exists`);
    const exists = directories.exists(path);
    res.status(exists ? 409 : 404).end();
});

app.get('/directories/files/checkpoints', (req, res) => {
    const path = req.query.path;
    console.info(`Looking for ${path} checkpoints`)
    const checkpoints = directories.content.checkpoints(path);
    if (checkpoints) res.json(checkpoints);
    else res.status(404).end();
});

app.get('/files/exists', (req, res) => {
    const path = req.query.path;
    console.info(`Checking if ${path} file exists`);
    const exists = directories.content.exists(path);
    res.status(exists ? 409 : 404).end();
})

app.post('/files', (req, res) => {
    const body = req.body;
    const path = req.query.path.replace('/', '');
    console.info(`Creating file for path ${path} with body ${JSON.stringify(body)}`);
    res.json(directories.content.create(path, body))
});

app.put('/files', (req, res) => {
    const body = req.body;
    const path = req.query.path;
    console.info(`Updating file for path ${path} with body ${JSON.stringify(body)}`);
    res.json(directories.content.put(path, body));
});

app.put('/files/rename', (req, res) => {
    let oldPath = req.query.old_path;
    let newPath = req.query.new_path;
    if (!oldPath.startsWith('/')) oldPath = `/${oldPath}`
    console.log(`Renaming ${oldPath} to ${newPath}`);
    res.json(directories.content.rename(oldPath, newPath));
})

app.post('/files/checkpoints', (req, res) => {
    const content = req.body.content;
    const path = req.query.path;
    console.log(`Creating checkpoint for path ${path} with content ${content}`);
    res.json(directories.content.putCheckpoint(path, content));
});

app.post('/directories', (req, res) => {
    const path = req.query.path;
    console.log(`Creating folder for path ${path}`);
    res.json(directories.create(path));
})

app.get('/type', (req, res) => {
    let path = req.query.path;
    const type = req.query.type;
    if (path.trim() === '' && type === 'directory') {
        res.status(200).end();
        return;
    }

    if (!path.startsWith('/')) {
        path = `/${path}`
    }

    console.log(`Checking is path ${path} is type of ${type}`)
    const isType = directories.content.isType(path, type);
    console.log(`${path} is type of ${type} ? ${isType}`)
    res.status(isType ? 200 : 400).end();
})

app.listen(port, () => {
    console.info(`Mocking server listening at http://localhost:${port}`);
});
