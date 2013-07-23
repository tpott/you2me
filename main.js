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
var Search = require('./model/search.js');

// inits
var app = express();
var conf = {
	'lang' : 'python',
	'port' : 1024
};

// unused: view/album.ejs view/playlist.ejs
var searchPage = fs.readFileSync('view/searchPage.html', 'utf8'),
	 redirectPage = fs.readFileSync('view/redirect.html', 'utf8'),
	 notFinPage = fs.readFileSync('view/notfinished.html', 'utf8');

var compiledRedirect = ejs.compile(redirectPage),
	 compiledNotFin = ejs.compile(notFinPage);

// configs
// TODO req.body isn't working
app.use(express.bodyParser()); // necessary for POST variable parsing
Search.setConfig(conf);

// routes
app.get('/', function(req, res) {
	res.end(searchPage);
});

app.get('/:uniqurl', function(req, res) {
	var url = req.params.uniqurl;
	res.setHeader('Content-Type', 'text/html');
	if (Search.urlExists(url)) {
		if (Search.history[url].isFinished()) {
			res.end(Search.history[url].html);
		}
		else {
			res.end(compiledNotFin({
				'url' : url
			}));
			//res.end('The search hasnt finished yet, refresh the page please.');
		}
	}
	else {
		//next();
		res.status(404);
	}
});

app.post('/search', function(req, res) {
	// currently needs to be redirectable on wikipedia
	//var searchText = 'Rodrigo_Y_Gabriela'; // TODO req.body isn't working
	var searchText = req.body.text; 
	var wiki = 'http://en.wikipedia.org/wiki/';

	// this will spawn a child process looking for wiki data
	var searchObj = new Search(searchText);
	var dataurl = wiki + searchText;

	res.setHeader('Content-Type', 'text/html');

	//res.write(ejs.render(redirectPage, { 
	res.write(compiledRedirect({ 
		'text' : searchText,
		'url' : searchObj.uniqueURL 
	}));
	/*res.write('You tried to search for: ');
	res.write(searchText + '\n<br /> ');
	res.write('ERROR: Unable to read post variables\n<br /> ');
	res.write('Redirecting to "<a href="' + searchObj.uniqueURL + '">');
	res.write(searchObj.uniqueURL + '</a>".');
	res.write('<script>setTimeout(function() { window.location = "');
	res.write(searchObj.uniqueURL + '"; alert("hi"); }, 1000);</script');*/
	res.end();
});

// execs
app.listen(conf.port);
console.log('Listening on port %d', conf.port);
