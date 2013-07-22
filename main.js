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
// TODO req.body isn't working
app.use(express.bodyParser()); // necessary for POST variable parsing

// routes
app.get('/', function(req, res) {
	res.end(searchPage);
});

app.get('/:uniqurl', function(req, res) {
	res.end('Unique URL! Thats awesome');
});

app.post('/search', function(req, res) {
	// currently needs to be redirectable on wikipedia
	var searchText = 'Rodrigo_Y_Gabriela'; // TODO req.body isn't working
	//var searchText = req.body.text; 
	var wiki = 'http://en.wikipedia.org/wiki/';

	res.write('You tried to search for: ');
	res.write(searchText + '\n<br /> ');
	res.write('ERROR: Unable to read post variables\n<br /> ');
	res.end();
});

// execs
app.listen(port);
console.log('Listening on port %d', port);
