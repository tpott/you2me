#!/usr/bin/env python

###############################################
# artistToHTML.py
#
# This is intended to be ran as a shell script.
# It should take a single argument (for now) 
# and print to stdout an html page that 
# represents the artist's discography and links
# for each track. 
#
# Trevor Pottinger
# Thu Mar 21 22:35:33 PDT 2013
###############################################

import sys

from wikiCrawler import Artist

def convertToHTML(info):
	"""Converts a 2 dimensional list into HTML. Requires
	1) each item in info is an Album
	1a) each Album has a name
	2) each item in an Album is a Track
	2a) each Track has a name
	2b) each Track has a link"""
	string = "<ul id=\"albums\">"
	for album in info:
		string += "<li><h2>" + album.name +"</h2><br /><ol>"
		for track in album:
			string += "<li><a href=\"" + track.link + \
					"\">" + track.name + "</a></li>"
		string += "</ol></li>"
	string += "</ul>"
	return string

def genHTML(artist):
	artistInfo = convertToHTML(artist.albums)
	print """
<html>
	<head>
		<title>{artistName}</title>
		<meta name="notes" content="you2me 0.0.1">
	</head>
	<body>
		<h1>{artistName}</h1>
		{artistInfo}
	</body>
</html>
""".format(artistName=artist.name, artistInfo=artistInfo)

if __name__ == '__main__':
	genHTML(Artist(sys.argv[1]))
