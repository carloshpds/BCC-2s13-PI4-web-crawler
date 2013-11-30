import urlparse
import urllib2
from termcolor import colored
from bs4 import BeautifulSoup
from data import Data

class DataExtractor:

	def __init__(self):

		self.path = ""
		self.actualURL = ""

		#LINKS OF RESOURCERS
		self.visitedUrls   			= []
		self.visitedImages     	= []
		self.visitedVideos   		= []
		self.visitedDocuments 	= []

		#Visited
		self.visitedIframes = []

		#DOCUMENTS
		self.targetTextFiles = []
		self.targetDocuments = ['www.slideshare.net/slideshow/']
		self.targetImages    = []
		self.targetVideos    = ['www.youtube.com', 'player.vimeo.com/video', 'youtube', 'vimeo' ]
		self.targetAudios    = []
		self.targetEbooks    = []


	def getData(self, url):
		
		data = Data()
		try:
			
			req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
			request = urllib2.urlopen(req)
			mime = request.info().getheader('Content-Type')		
			code = request.code

			print(colored('[' + mime + '] ' + url, 'yellow'))

			if code is 200:
				if 'text/html' in mime:

					html = request.read()
					data = self.parse(html, url)
					
				else:
					#ANALYSIS TYPE
					data.url = url
					data.type = mime

			elif code is 400:
				data.broke = True
		
		except urllib2.HTTPError as e:
			self.messageError(e)
			data.broke = True
		except UnicodeEncodeError as e :
			self.messageError(e)
			data.broke = True
		except ValueError as e:
			self.messageError(e)
			data.broke = True
		except urllib2.URLError as e:
			self.messageError(e)
			data.broke = True
	
		return data 

	def messageError(self, e):
		print(colored(e, 'red'))
			
	def parse(self, html, path):

		self.actualURL = path

		html = BeautifulSoup(html)
		DOMElementURL 	  = html.find_all('a', href=True)
		DOMElementImages  = html.find_all('img', { "src" : True })
		DOMElementIframes = html.find_all('iframe', {"src" : True})

		data = Data()
		data.url  	= [path]
		data.urls 	= self.getUrls(DOMElementURL)
		data.images = self.getImages(DOMElementImages)

		iframe = self.getDocuments(DOMElementIframes)

		if iframe is not None:
			data.documents = iframe['documents']
			data.videos  	 = iframe['videos']

		return data

	def getUrls(self, DOMElementURL):

		contentUrl  = []
		
		#Recupera todas as URLS
		for url in DOMElementURL:
			
			url = urlparse.urljoin(self.actualURL, url['href'])
			containsPath = self.path in url 
			isVisited = url not in self.visitedUrls 

			if containsPath and isVisited:
				contentUrl.append(url)

		return contentUrl

	def getImages(self, DOMElementImages):

		contentImg  = []
	
		#Recupera todas as IMGS
		for img in DOMElementImages:	
			
			img = urlparse.urljoin(self.actualURL, img['src'])
			containsPath = self.path in img
			isVisited  = img not in self.visitedImages

			if containsPath and isVisited:
				contentImg.append(img)
				self.visitedImages.append(img)

		return contentImg

	def getDocuments(self, DOMElementIframes):
		
		contentVid  = [] 
		contentDoc  = []

		#PROCURA ESPECIAL
		for iframe in DOMElementIframes :         
			iframeSrc = str(iframe["src"])

			#PROCURA POR VIDEOS
			for target in self.targetVideos:
				if target in iframeSrc:
					print(colored('VIDEO :' + iframeSrc, 'red')) 
					contentVid.append(iframeSrc)
					self.visitedVideos.append(iframeSrc)

			#PROCURA POR DOCS
			for target in self.targetDocuments:	
				if target in iframeSrc:
					print(colored('DOCUMENT: ' + iframeSrc, 'red'))
					contentDoc.append(iframeSrc)
					self.visitedDocuments.append(iframeSrc)

		data = {
			'videos' : contentVid,
			'documents' : contentDoc
		}

		return data

