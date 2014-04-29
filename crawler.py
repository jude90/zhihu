import traceback
import re
from threading import Thread
import time
from Queue import Queue as Que
class Crawler(object):
	"""docstring for Crawler"""
	def __init__(self, route, RDB):
		
		self.route = route
		self.visited = RDB #must be a redis client
		self.todolst = Que(100) 

	def put(self, item):
		self.todolst.put(item)

	def _fetch(self, timeout=10):
		todo = self.todolst
		route = self.route
		visited = self.visited
		try:
			while True:
				url = todo.get(timeout=timeout)
				handler = route.match(url)

				if not handler: continue
				hdl = handler(url)
				next_urls = hdl.get()
				visited.set(url,url)
				
				time.sleep(0.5)
				for  ul in next_urls :
					#if not visited.exists(url):
					if todo.not_full:todo.put(ul) 
				
		except :
			#fix me
			traceback.print_exc()
			return 

	def go(self,num,timeout=60):
		for i in xrange(num):
			g = Thread(target=self._fetch)
			g.start()
		g.join()

class Route(object):
	"""docstring for Route"""
	def __init__(self):
		self.map = []

	def __call__(self,path):
		if not path.endswith('$'): path +='$'

		re_path = re.compile(path)
		def _(func):
			self.map.append((re_path, func))
			return func
		return _

	def match(self,url):
		for r, f in self.map:
			m = r.match(url)
			if m:
				return f
		print "WARNING :",url,"not match any handler"
		return None

class Handler(object):
	"""baseclass for Handler"""
	def __init__(self, url ):
		self.url = url
		
	def get(self, url):
		pass