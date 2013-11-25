import urllib2
from bs4 import BeautifulSoup
from resources import Resourcer

class DataExtractor:
	
	def getData(self, url):

		body = urllib2.urlopen(url).read()
		html = BeautifulSoup(body)

		contentURLS	= []
		contentIMGS	= []
		
		#DOM ELEMENTS 

		DOMElementLink 		= html.find_all('a', href=True)
		DOMElementImg  		= html.find_all('img', { "src" : True } )
		DOMElementIframes 	= html.find_all('iframe', {"src" : True})

		#Recupera todas as URLS
		for link in DOMElementLink:
			
			link = urlparse.urljoin(url, link['href'])

			containsURLRoot      = url in link
			historyLocalVisited  = link not in unreadURLs
			historyRemoteVisited = link not in self.visitedUrls 

			if containsURLRoot and historyLocalVisited and historyRemoteVisited:
				unreadURLs.append(link)
				Resourcer.quantidadeURL += 1

		#Recupera todas as IMGS
		for img in DOMElementImg:	
			img = img['src']	

			historyLocalVisited  = img not in contentIMGS
			historyRemoteVisited = img not in self.visitedImages

			if historyLocalVisited and historyRemoteVisited:
				contentIMGS.append(img)
				self.visitedImages.append(img)

				#print(img)

		# for textFile in targetTextFiles:
		# 	print(textFile)

		# for document in targetDocuments:
		# 	print(document)
	
		# for image in targetImage :
		# 	print(image)

		self.getIframes(DOMElementIframes)

		 	
		# for audio in targetAudio :
		# 	print(audio)

		# for ebooks in targetEbooks: 
		# 	print(ebooks)

		data = Data()
		data.url = unreadURLs
		data.image = contentIMGS

		return data

	def getIframes(self, DOMElementIframes):
		
		for iframe in DOMElementIframes :         
			iframeSrc = str(iframe["src"])
			hasType   = False

			if iframeSrc not in self.visitedIframes:
				self.visitedIframes.append(iframeSrc)

				# Videos
				hasType = self.getVideo(iframeSrc)

				# Documents
				if not hasType : hasType = self.getDocument(iframeSrc)
				else: continue

	def getVideo(self, src ):
		print 'TRY - getVideo: ' + src
		return self.getSomething(src,self.targetVideos,self.visitedVideos)

	def getDocument(self, src):
		print 'TRY - getDocument: ' + src
		return self.getSomething(src,self.targetDocuments,self.visitedDocuments)

	def getSomething(self, src, selfTarget, selfVisited  ):
		for target in selfTarget:
			if src not in selfVisited :
				if target in src :
					selfVisited.append(src)
					print('=================\nI FOUND SOMETHING: ' + src + '\n=================')
					return True
				
			else:
				return True
