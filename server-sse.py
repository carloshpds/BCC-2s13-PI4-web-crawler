import cherrypy
import os.path
import json
import time
from cherrypy.lib.static import serve_file
from crawler_dao import CrawlerDAO
from crawler import Crawler

current_dir = os.path.dirname(os.path.abspath(__file__))
public_dir  = os.path.join(current_dir, 'public/dist')

class Root():

	def __init__(self):
		self.dao = CrawlerDAO()
		
	@cherrypy.expose
	def index(self):
		#return serve_file(os.path.join(current_dir, 'index.html'), content_type='text/html')
		return serve_file(os.path.join(public_dir , 'index.html'), content_type='text/html')

	@cherrypy.expose
	def start(self, site):

		cherrypy.request.headers["Content-Type"] = 'utf-8'

		dao = CrawlerDAO()
		dao.reset()

		crawler = Crawler(dao, 'http://' + site)
		crawler.run()
 
		#FINISHED CONNECTION
		dao.connection.close()

	@cherrypy.expose
	def yieldResource(self):

		cherrypy.response.headers["Content-Type"] = "text/event-stream"

		def content():

			#Server time poooling
			for pooling in xrange(0, 5):
				time.sleep(1)

			return "event: time\n" + "data: " + str(self.dao.select()) + "\n\n";

		return content()

	yieldResource._cp_config = {'response.stream' : True, 'tools.encode.encoding' : 'utf-8'}

if __name__ == '__main__':

	dao = CrawlerDAO()	
		
	pageroot = Root()

	conf = {
			'/' : {
			 	'tools.encode.encoding': 'utf-8',
				'response.timeout' :  1000000,
				'tools.staticdir.root': current_dir
			},
 
			'/feed': {
				'tools.staticdir.on' : True,
				'tools.staticdir.dir': os.path.join(current_dir, 'public'),
				'tools.staticdir.content_types': {
					'rss' : 'application/json',
					'atom': 'application/json'
				},
				
			},

			'/scripts' : {
				'tools.staticdir.on' : True,
				'tools.staticdir.dir': os.path.join(public_dir,'scripts' )
			},

			'/styles' : {
				'tools.staticdir.on' : True,
				'tools.staticdir.dir': os.path.join(public_dir,'styles' )
			},

			'/views' : {
				'tools.staticdir.on' : True,
				'tools.staticdir.dir': os.path.join(public_dir, 'views' )
			}
		}



	cherrypy.quickstart(pageroot, config=conf)
