import urlparse
import urllib2
from termcolor import colored
from bs4 import BeautifulSoup
from data import Data

class DataExtractor:

	def __init__(self):

		self.path = ""
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
		self.targetVideos    = ['www.youtube.com', 'player.vimeo.com/video' ]
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

		except UnicodeEncodeError as e :

			print(colored(e, 'red'))
			data.broke = True

		return data 
			
	def parse(self, html, path):
		
		html = BeautifulSoup(html)
		DOMElementURL 	  = html.find_all('a', href=True)
		DOMElementImages  = html.find_all('img', { "src" : True } )
		DOMElementIframes = html.find_all('iframe', {"src" : True})

		contentUrl  = []
		contentImg  = []
		contentVid  = []
		contentDoc  = []
 
		#Recupera todas as URLS
		for url in DOMElementURL:
			
			url = urlparse.urljoin(path, url['href'])
			containsPath = self.path in url
			isVisited = url not in self.visitedUrls 

			if containsPath and isVisited:
				contentUrl.append(url)

		#Recupera todas as IMGS
		for img in DOMElementImages:	
			
			img = urlparse.urljoin(path, img['src'])

			containsPath = self.path in img
			isVisited  = img not in self.visitedImages

			if containsPath and isVisited:
				contentImg.append(img)
				self.visitedImages.append(img)	

		#PROCURA ESPECIAL
		for iframe in DOMElementIframes :         
			iframeSrc = str(iframe["src"])

			#PROCURA POR VIDEOS
			for target in self.targetVideos:
				containsTarget = target in iframeSrc
				contentVid.append(iframSrc)
				self.visitedVideos.append(iframeSrc)

			#PROCURA POR DOCS
			for target in self.targetDocuments:	
				containsTarget = target in iframeSrc
				contentDoc.append(iframSrc)
				self.visitedDoc.append(iframeSrc)

		data = Data()
		data.url  = [path]
		data.urls = contentUrl
		data.img  = contentImg
		data.doc  = contentDoc
		data.vid  = contentVid

		return data

	#def analysis(self):

	def getIframes(self, DOMElementIframes):
		
		for iframe in DOMElementIframes :         
			
			iframeSrc = str(iframe["src"])
			hasType = False

			if iframeSrc not in self.visitedIframes:
				self.visitedIframes.append(iframeSrc)
				
				# Videos
				hasType = self.getVideo(iframeSrc)

				# Documents
				if not hasType : 
					hasType = self.getDocument(iframeSrc)
				else: continue

	# def getVideo(self, src, content ):
	# 	print 'TRY - getVideo: ' + src
	# 	return self.getSomething(src,self.targetVideos,self.visitedVideos)

	# def getDocument(self, src):
	# 	print 'TRY - getDocument: ' + src
	# 	return self.getSomething(src,self.targetDocuments,self.visitedDocuments)

	# def getSomething(self, src, selfTarget, selfVisited  ):
	# 	for target in selfTarget:
	# 		if src not in selfVisited :
	# 			if target in src :
	# 				selfVisited.append(src)
	# 				return True
				
	# 		else:
	# 			return True
