'use strict';

if (process.env.XSSHUNTER_NODE_ENV !== 'docker') {
  require('dotenv').config({ path: '../.env' });
}
const http = require('http');
const get_app_server = require('./app.js');
const database = require('./database.js');

const database_init = database.database_init;

(async () => {
  // Ensure database is initialized.
  await database_init();

  const app = await get_app_server();
  const port = process.env.XSSHUNTER_PORT || 3000; // Fallback to 3000 if the PORT variable is not set

  // Create HTTP server
  http.createServer(app).listen(port, function () {
    console.log(`HTTP server running on port ${port}`);
  });
})();
