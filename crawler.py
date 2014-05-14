import traceback
import re
from threading import Thread
import time
from Queue import Queue as Que
from Queue import Empty, Full
from redis import ConnectionError
import random
class Crawler(object):
	"""docstring for Crawler"""
	def __init__(self, route, RDB):
		
		self.route = route
		self.visited = RDB #must be a redis client
		self.todolst = Que(100) 

	def put(self, item):
		self.todolst.put(item)

	def _fetch(self, timeout=10):
		def select(tag):
			while True:
				key = visited.randomkey()
				if visited.get(key) == tag: break					
			return key

		todo = self.todolst
		route = self.route
		visited = self.visited
		try:
			while True:
				url = todo.get(timeout=timeout)
				handler = route.match(url)

				if not handler: continue
				hdl = handler(url)
				visited.set(url,"done")

				
				time.sleep(random.random())
				new_urls = hdl.get()
				[visited.set(ul, "todo") for ul in new_urls if not visited.exists(ul)]
				while not todo.full():
					todo.put(select('todo'))

					

		except Empty,ConnectionError:
			
			traceback.print_exc()
			return 

	def go(self,num,timeout=60):
		for i in xrange(num):
			g = Thread(target=self._fetch)
			g.start()
		g.join()

	def stop(self):pass



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

if __name__ == '__main__':
	
	from redis import Redis
	from zhihu_fetch import People, Question,route
	urls =['/question/22624255','/question/20584119','/question/21084111']
	
	RDB = Redis(db=2)


	#spider = Spider(route, RDB)
	cola = Crawler(route,RDB)
	for i in xrange(50):
		key = RDB.randomkey()
		if RDB.get(key) =="todo":
			cola.put(key)
	cola.go(6)