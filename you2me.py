###############################################
# you2me.py
#
# 2012-07-21
###############################################

import dispatch
import wikiCrawler
import youSearcher

class blackbox(object):
	def __init__(self):
		pass

	def get(self, artist):
		"""Retrieves various mp3 files for the tracks that are listed
		on the artist's wikipedia pages."""
		pass

if __name__ == '__main__':
	import sys
	box = blackbox()
	result = box.get(sys.argv[1])
	print result
