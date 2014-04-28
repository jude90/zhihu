#coding:utf-8
import gevent.monkey
gevent.monkey.patch_all()
from gevent.queue import Empty, Queue
from gevent import sleep , spawn, joinall
import requests
from urlparse import urlparse, parse_qs
import re

class Spider(object):
	"""docstring for Spider"""
	def __init__(self, route, RDB):
		
		self.route = route
		self.visited = RDB #must be a redis client
		self.todolst = Queue(100) 

	def _fetch(self, timeout):
		todo = self.todolst
		route = self.route
		visited = self.visited
		try:
			while True:
				url = todo.get(timeout=timeout)
				handler = route.match(url)
				hdl = handler(url)
				next_urls = hdl.get()
				visited.set(url,url)
				[todo.put(url) for  url in next_urls if not visited.exists(url)]
				gevent.sleep(1)
		except Empty:
			#fix me
			return 

	def run(self,num,timeout=60):
		self.workers = [spawn(self._fetch,timeout) for i in xrange(num)]
		joinall(self.workers)

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

route = Route()
spider = Spider(route)		
		








