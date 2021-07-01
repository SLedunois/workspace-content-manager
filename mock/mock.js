const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

const Directories = require('./directories');
const directories = new Directories(); 7

app.use(bodyParser.json());

app.get("/directories", (req, res) => {
    console.log(`Looking for directory content`);
    res.json(directories.data);
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
})

app.post('/files/checkpoints', (req, res) => {
    const content = req.body.content;
    const path = req.query.path;
    console.log(`Creating checkpoint for path ${path} with content ${content}`);
    res.json(directories.content.putCheckpoint(path, content));
})

app.listen(port, () => {
    console.info(`Mocking server listening at http://localhost:${port}`);
});
