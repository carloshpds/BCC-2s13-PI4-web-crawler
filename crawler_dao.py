import sqlite3 
import json
from termcolor import colored
from data import Data
from time import gmtime, strftime

class CrawlerDAO:

	def __init__(self):

		self.visited = []
		
		self.queueSync = []

		self.connection = sqlite3.connect('crawler.db', check_same_thread=False)
		self.crawler = self.connection.cursor()

	def reset(self):

		sql = 'DROP TABLE IF EXISTS data'
		self.crawler.execute(sql)
		self.createDataTable()

	def createDataTable(self):

		query = 'CREATE TABLE data (id INTEGER PRIMARY KEY, json TEXT, time TEXT, visited TEXT)'
		self.crawler.execute(query)

	def insertDataJSON(self, json):

		data = { 
			'json' : json , 
			'time' : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
			'visited' : False
		}

		self.crawler.execute("INSERT INTO data (json, time, visited) VALUES (?, ?, ?)", (data['json'], data['time'], 'False') )
		self.connection.commit()

		
	def select(self):

			getJsonSQL  = "SELECT id, json FROM data WHERE visited = 'False' ORDER BY id LIMIT 1"
			
			self.crawler.execute(getJsonSQL)
			datas = self.crawler.fetchone()

			dataId 	 = data[0]
			dataJson = data[1]

			print(colored('[LOG] SYNC TIME OBJETO ' + str(dataId) + '.', 'green'))

			self.crawler.executem("UPDATE data SET visited = 'True' WHERE id = ?", (dataId,))
			self.connection.commit()
			
			return dataJson
