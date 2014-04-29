import traceback
import re
from threading import Thread
import time
from Queue import Queue as Que
from Queue import Empty, Full
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
				
				time.sleep(0.1)
				[todo.put(ul,timeout=timeout+10) for ul in next_urls if  not (visited.exists(ul) or todo.full())]				
		except Empty:
			#fix me
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
	urls =['/question/22624255','/question/20584119','/question/19861840']
	
	RDB = Redis(db=1)


	#spider = Spider(route, RDB)
	cola = Crawler(route,RDB)
	for item in urls:
		cola.put(item)
	cola.go(6)