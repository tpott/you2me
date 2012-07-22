###############################################
# wikiCrawlser.py
#
# 2012-07-21
###############################################

_api = 'http://en.wikipedia.org/w/api.php?'
_query = 'action=query'
_xml = 'format=xml'
_redirects = 'redirects'
_titles = 'titles=%s' # allows for string substitution


import mechanize as mech
from BeautifulSoup import BeautifulSoup as bs

class artistInfo(object):
	def __init__(self):
		self.br = mech.Browser()
		self.br.addheaders = [('User-agent', 'PyBros_Music')]
		self.br.set_handle_robots(False)

	def getTracks(self, artist_name):
		"""Returns a list of tracks, where each one represents
		some track info that should be retrieved."""
		escArtist = artist_name.replace(' ', '_')
		qurl = _api + '&'.join([_query, _xml, _redirects, _titles])
		qurl = qurl % escArtist
		url = 'http://en.wikipedia.org/wiki/%s' % escArtist
		try:
			print url
			self.br.open(url)
		except Exception as e:
			print 'Unable to retrieve: %s' % artist_name
			print e
			return []
		soup = bs(self.br.response().read())
		try:
			h2 = soup.find(id='Discography').parent
			h3start = h2.nextSibling.nextSibling # h2.nextSibling is '\n'
		except Exception as e:
			print 'Unable to find Discography'
			print e
			return []




