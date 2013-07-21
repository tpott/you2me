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
}
