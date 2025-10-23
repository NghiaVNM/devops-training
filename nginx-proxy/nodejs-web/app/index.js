const express = require('express');
const app = express();
const port = 80;

app.use(express.json());

app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

app.get('/', (req, res) => {
  res.json({
    message: 'Hello World from Node.js!',
    version: '1.0.0'
  });
});

app.get('/healthz', (req, res) => {
  res.json({  status: 'ok' });
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Server running on port ${port}`);
});