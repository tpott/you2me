###############################################
# youSearcher.py
#
# 2012-07-21
###############################################
import urllib2

class youtube(object):
	def __init__(self):
		pass

	def search(self,artist, track):
         YTSERVER = "https://gdata.youtube.com/feeds/api/videos?"
         Search = YTSERVER + "?%s+%s" % (artist, track)
         print Search
         SearchReq = urllib2.Request(url=YTSERVER,data=Search)
         results = urllib2.urlopen(SearchReq)
         print results.read()
