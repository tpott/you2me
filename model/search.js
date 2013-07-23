/**
 * search.js
 *
 * Represent any search as an object. These search objects (sobjs) will then 
 * be stored in a separate object. The storage object will most likely be
 * indexed by the search text in lowercase form. Nested inside that will be
 * an object that is indexed by the time of search. 
 *
 * Trevor Pottinger
 * Sun Jul 21 15:42:20 PDT 2013
 */

var crypto = require('crypto'),
	 proc = require('child_process');

var ncalls = 0;

// copied from
// https://github.com/tpott/butter-star/blob/master/server/objects/random.js
function random(length) {
	// generate a random url
	var sha = crypto.createHash('sha256'); // hash factory
	sha.update(ncalls.toString() + Date.now(), 'utf8'); // feed the factory
	var str = sha.digest('base64') // read and lock factory
		.slice(0,length)			// make shorter
		.replace(/\+/g, "-")	// replace non-url friendly characters
		.replace(/\//g, "_")
		.replace(/=/g, ",");

	ncalls++;
	return str;
}

/**
 * searchText- what was searched for. v0.1 asks for an artist url from 
 * 	it's wiki page, i.e. no searching :'(
 * searchTime- a high-res time object, represented as an array of integers.
 * 	index 0 is time in seconds, index 1 is remainder in nanoseconds
 * uniqueURL- used to display the results
 */
function SearchObject(searchText) {
	this.searchText = searchText;
	this.searchTime = process.hrtime();
	this.uniqueURL = random(8);
	this.config = SearchObject.conf;

	this.html = '<html><h1>No results :(</h1></html>';
	this._partial = '';
	this.finished = false;

	this.start();

	history[this.uniqueURL] = this;
}

SearchObject.prototype.start = function() {
	var self = this; 

	switch(this.config.lang) {
		case 'python':
			var child = proc.spawn('./artistToHTML.py', [ this.searchText ]);
			child.stdout.on('data', function(buf) {
				self._partial += buf.toString();
			});
			child.on('close', function() {
				self.html = self._partial;
				self.finished = true;
			});
			break;
		default:
			self.html = self._partial;
			self.finished = true;
			break;
	}
};

SearchObject.prototype.isFinished = function() {
	return this.finished;
};

function setConfig(conf) {
	SearchObject.conf = conf;
};

function urlExists(url) {
	return url.length == 8;
}

var history = {};
SearchObject.conf = {};

module.exports = SearchObject;
module.exports.urlExists = urlExists;
module.exports.history = history;
module.exports.setConfig = setConfig;
