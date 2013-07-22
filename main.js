/**
 * main.js
 *
 * Trevor Pottinger
 * Sun Jul 21 15:38:42 PDT 2013
 */

// imports
var express = require('express'),
	 ejs = require('ejs'),
	 fs = require('fs');

// inits
var app = express();
var port = 1024;

var searchPage = fs.readFileSync('view/searchPage.html');

// configs
app.use(express.bodyParser()); // necessary for POST variable parsing

// routes
app.get('/', function(req, res) {
	res.end(searchPage);
});

app.get('/:uniqurl', function(req, res) {
	res.end('Unique URL! Thats awesome');
});

app.post('/search', function(req, res) {
	res.write('You searched for "' + req.body.toString() + '"'); 
	res.end();
});

// execs
app.listen(port);
console.log('Listening on port %d', port);
