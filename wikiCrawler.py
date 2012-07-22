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

_wiki = 'http://en.wikipedia.org'

def prune(a, x):
	if x != None:
		a.append(x)
	return a

def table2dict(tbl):
	"""Returns a list of dictionaries. This table requires the first
	row contain headers for the columns"""
	rows = tbl.findAll('tr')
	row1 = rows[0]
	headers = row1.findAll('th')
	keys = map(lambda h: h.string, headers)
	rows = rows[1:]

def table2list(tbl):
	"""Returns a list of lists"""
	pass

import mechanize as mech
from BeautifulSoup import BeautifulSoup as bs

class artistInfo(object):
	def __init__(self):
		self.br = mech.Browser()
		self.br.addheaders = [('User-agent', 'PyBros_Music')]
		self.br.set_handle_robots(False)

	def _parse(self, html):
		soup = bs(html)
		table = soup.find('table', class='tracklist')
		tracks = table2dicts(table)
		return map(lambda d: track(d), tracks)

	def _links(self, link):
		album_name = link.string
		if album_name == None:
			return None
		def _href(a, x):
			if a == None and x[0] == 'href':
				return x[1]
			else:
				return a
		relurl = reduce(_href, link.attrs, None)
		a = album()
		a['title'] = album_name
		a['url'] = _wiki + relurl
		return a

	def _tracks(self, p):
		"""p points to the current tag. pages is a list of tuples. the 
		tuples are group * list of track info"""
		self.pages = []
		grouping = ''
		while p.name != 'h2':
			if p.name == 'h3':
				grouping = p.contents[2].string
			elif p.name == 'ul':
				links = p.findAll('a')
				# appends a tuple, string*list
				tup = (grouping, reduce(prune, map(self._links, links), []))
				self.pages.append(tup)
			p = p.nextSibling
			if p == '\n':
				p = p.nextSibling
		self.pages = reduce(prune, self.pages, [])
		albums = [ album for group in self.pages for album in group[1] ]
		for album in albums:
			try:
				self.br.open(album['url'])
				# _parse returns a list of track objects
				album['tracks'] = self._parse(self.br.response().read())
			except:
				continue
		self.albums = albums
		return albums

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
		return self._tracks(h3start)


class album(dict):
	def __init__(self):
		self.tracks = []


class track(dict):
	pass
