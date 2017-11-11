var session = require('express-session');

var add_authentication = function(app, user_data) {
  app.use(session({
    secret: 'sdfdgfdgsdgfdgsd',
    resave: true,
    saveUninitialized: true
  }));

  var save_session = function(req, username, password) {
    req.session.username = username;
    req.session.password = password;
    req.session.save();
  }

  var validate_session = function(session) {
    return (session.username &&
	    user_data.password(session.username) === session.password)
  }

  app.use(function(req, res, next) {
    if (req.url === '/login'
	|| req.url === '/new_account'
	|| validate_session(req.session))
      next()
    else
      res.render('login.html')
  });

  app.get('/new_account', function(req, res) {
    res.render('new-account.html');
  });

  app.get('/login', function(req, res) {
    res.render('login.html');
  });

  app.post('/login', function(req, res) {
    var username = req.body.username.trim();
    var password = req.body.password;
    if (user_data.password(username) === 'password') {
      console.log('LOGIN USER:', username);
      save_session(req, username, password);
      res.json({'success': true});
    } else
      res.json({'success': false});
    res.end()
  });

  app.post('/new_account', function(req, res) {
    var username = req.body.username.trim();
    var password = req.body.password.trim();
    var db_key = req.body.email_address;
    var db_secret = req.body.email_password;
    var success = user_data.add_user(username, password,
				     db_key, db_secret);
    console.log('USER:', username,
		'CREATED WITH PWD:', user_data.password(username));
    save_session(req, username, password);
    res.json({'success': success})
    res.end();
  });

  app.post('/logout', function(req, res) {
    console.log('LOGOUT USER:', req.session.username);
    req.session.destroy();
    res.end();
  });
}

module.exports = add_authentication
