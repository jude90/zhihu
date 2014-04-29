#coding:utf-8
import gevent.monkey
gevent.monkey.patch_all()
from gevent.queue import Empty, Queue
from gevent import sleep , spawn, joinall 
import requests
from urlparse import urlparse, parse_qs
import re
import traceback


class Spider(object):
	"""docstring for Spider"""
	def __init__(self, route, RDB):
		
		self.route = route
		self.visited = RDB #must be a redis client
		self.todolst = Queue() 

	def put(self, item):
		self.todolst.put(item)

	def _fetch(self, timeout):
		todo = self.todolst
		route = self.route
		visited = self.visited
		try:
			while True:
				url = todo.get(timeout=timeout+10)
				handler = route.match(url)
				if not handler: continue
				hdl = handler(url)
				next_urls = hdl.get()
				visited.set(url,url)
				gevent.sleep(0.5)
				#todo.put(next_urls.pop())
				for  ul in next_urls :
					if not visited.exists(ul):
						todo.put(ul,timeout=10)

				gevent.sleep(0.5)
		except :
			#fix me
			traceback.print_exc()
			return 

	def go(self,num,timeout=60):
		self.workers = [spawn(self._fetch,timeout) for i in xrange(num)]
		gevent.sleep(1)
		self.workers[0].join()

	#fix me
	def stop(self):
		for worker in self.workers:
			workers.kill()

		self.visited.save()

class Handler(object):
	"""baseclass for Handler"""
	def __init__(self, url ):
		self.url = url
		
	def get(self, url):
		pass
		

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


if __name__ == '__main__':
	from redis import Redis
	from zhihu_fetch import People, Question,route
	urls =['/people/xu-chi-45','/question/20664147','/question/21441534','/people/fengduan']

	RDB = Redis(db=1)
	#spider = Spider(route, RDB)
	spider = Spider(route,RDB)
	for item in urls:
		spider.put(item)
	spider.go(6)		








