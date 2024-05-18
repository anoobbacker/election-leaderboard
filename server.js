
rt { handler } from './build/handler.js';
import express from 'express';
import https from 'https';
import fs from 'fs';

const app = express();

// Load SSL certificates
const options = {
   key: fs.readFileSync('/path/to/your/ssl.key'),
     cert: fs.readFileSync('/path/to/your/ssl.cert')
};

app.use(handler);

https.createServer(options, app).listen(443, () => {
   console.log('Server is running on port 443');
});

