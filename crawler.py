import time
import json

from termcolor import colored
from crawler_dao import CrawlerDAO

from data import Data 
from data_extractor import DataExtractor

class Crawler():
	
	def __init__(self, crawlerDAO):

		self.url = ""

		self.crawlerDAO =  crawlerDAO
		self.visited		= []
		self.extractor  = DataExtractor()

	def run(self):

		#url = 'http://' + Resourcer.site
		url = 'http://www.dclick.com.br'
		#self.path = url
		urls = [url]

		print(colored('INICIANDO CRAWLING NO SITE:' + url, 'green'))
		start = time.time()

		self.search(urls)

		end = time.time() - start
		# Final Calcs
		
		print(colored('[LOG] SUCCESS FINISHED CRAWL', 'green'))
		print('-------------------------------------------------------------')
		print('BUSCA TERMINOU - TEMPO DE BUSCA: ' + str(end / 60))  
		print('-------------------------------------------------------------')

	def sync(self, data):
		
		#Serializa objeto data em JSON
		jsonDATA = json.dumps(data, default=lambda o: o.__dict__)
		self.crawlerDAO.insertDataJSON(jsonDATA)
	
	def search(self, urls):

			for url in urls:
				if url not in self.visited:

					data = Data()
					data = self.extractor.getData(url)
			
					#Adiciona novas URLS achadas no processo de getData.
					urls = urls + data.toCrawl
					data.toCrawl = []

					#Sync com o client novas informacoes.
					self.sync(data)

					self.visited.append(url)
					self.search(urls)
