var express = require('express');
var path = require('path');

var index = require('./routes/index');
var app = express();

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

app.use('/', index);
app.use((req, res) => {
  console.log(">> server: other case routing, back to browser");
  res.sendFile('index.html', {root: path.join(__dirname, '../client/build')});
});
// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;
