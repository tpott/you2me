###############################################
# wikiCrawlser.py
#
# 2012-07-21
###############################################

WIKIPEDIA = 'http://en.wikipedia.org'

import mechanize as mech
from BeautifulSoup import BeautifulSoup as bs

class Artist(object):
	def __init__(self, name):
		self.name = name
		self.albums = []
		self.scrape()

	def scrape(self):
		"""Scrape wikipedia for the album and track info, and
		then scrape youtube for track links"""

		# create Mechanize browser
		br = mech.Browser()
		br.addheaders = [('User-agent', 'PyBros_Music')]

		artist_name = self.name
		escArtist = artist_name.replace(' ', '_')

		# create escaped url
		escaped_url = WIKIPEDIA + '/wiki/%s' % escArtist

		# load artist page
		try:
			br.open(escaped_url)
		except Exception as e:
			print 'Unable to find page for %s' % self.name
			return 
		#print self.name
		soup = bs(br.response().read())

		# look for albums section 
		try:
			h2 = soup.find(id='Discography').parent
			h3start = h2.nextSibling.nextSibling # h2.nextSibling is '\n'
		except Exception as e:
			print 'Unable to find albums for %s' % self.name
			return 

		p = h3start # p will iterate through html DOM elements

		# for each element until the next wiki section
		while p.name != 'h2':
			# TODO compare with output of br.links()
			if p.name == 'ul': # list of links!
				links = p.findAll('a')
				for link in links:
					album = Album(str(link.contents[0]), self, link.get('href'))
					self.albums.append(album)
			else:
				pass
			p = p.nextSibling
			if p == '\n':
				p = p.nextSibling
		
		# for each album, scan the album page
		for i in range(len(self.albums)):
			try:
				br.open(WIKIPEDIA + self.albums[i].link)
			except:
				continue # skip album if no data is available
			#print self.albums[i].name
			soup = bs(br.response().read())
			table = soup.find('table', attrs={'class':'tracklist'})

			# each row in this magical table should be a song
			rows = table.findAll('tr')
			for row in rows:
				cols = row.findAll('td')
				if len(cols) != 3:
					# then I don't know what to do with this...
					continue
				# .contents[0] is cause beautifulsoup isn't that smart ;)
				try:
					number = str(cols[0].contents[0])
				except:
					number = ''
				try:
					name = str(cols[1].contents[0])
				except:
					name = ''
				try:
					length = str(cols[2].contents[0])
				except:
					length = ''
				track = Track(number, name, self.albums[i], length)
				self.albums[i].tracks.append(track)

		# done scraping =)

class Album(object):
	"""Album.name is the name of the album
	Album.artist is a reference to the parent object
	Album.link is the supposed wikipedia link"""
	def __init__(self, name, artist, link):
		self.name = name
		self.artist = artist
		self.link = link
		self.tracks = []
		self.i = -1
		#self.next = self.__next__

	def __iter__(self):
		return self

	def next(self):
		if self.i < len(self.tracks) - 1:
			self.i += 1
			return self.tracks[self.i]
		else:
			raise StopIteration

	def __str__(self):
		return self.name

class Track(object):
	def __init__(self, trackno, name, album, length):
		self.trackno = trackno
		self.name = name
		self.album = album
		self.length = length
		self.link = ''

	def findLink(self):
		"""Searches Youtube, given this track's name and
		the album's name."""
		pass
