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

def genHTML(artist):
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
""".format(artistName= artist.name, artistInfo= artist.info)

if __name__ == '__main__':
	genHTML(Artist(sys.argv[1]))
