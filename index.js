var express = require('express');
var body_parser = require('body-parser');
var mongoose = require('mongoose');

var UserData = require('./js/user-data.js');
var add_authentication = require('./routes/authentication.js');
var add_pages = require('./routes/pages.js');


var app = express();
app.use(body_parser.json());

app.set('views', __dirname + '/public');
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use(express.static(__dirname + '/public'));

mongodb_uri = process.env.MONGODB_URI || 'mongodb://localhost/whack2017';
console.log('CONNECTING TO DB URI', mongodb_uri);
mongoose.connect(mongodb_uri);
var db = mongoose.connection;

db.once('error', function(err) {
  console.log('MONGODB CONNECTION ERROR', err);
});

db.once('open', function() {
  user_data = UserData();
  add_authentication(app, user_data);
  //add_pages(app);
})


app_port = process.env.PORT || 3000;
app.listen(app_port, function() {
  console.log('LISTENING ON PORT', app_port);
});
