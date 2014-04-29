#coding:utf-8
import gevent.monkey
gevent.monkey.patch_all()
from gevent.queue import Empty, Queue, Full
from gevent import sleep , spawn, joinall 
import requests
from urlparse import urlparse, parse_qs
import re
import traceback
import json

class Spider(object):
	"""docstring for Spider"""
	def __init__(self, route, RDB):
		
		self.route = route
		self.visited = RDB #must be a redis client
		self.todolst = Queue(100) 

	def put(self, item):
		self.todolst.put(item)

	def _fetch(self, timeout):
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
				gevent.sleep(0.1)
				
				[todo.put(ul,timeout=timeout+10) for ul in next_urls if  not (visited.exists(ul) or todo.full())]
		except Empty,Full:						
		#except :
			#fix me
			traceback.print_exc()
			return 
		

	def go(self,num,timeout=60):
		self.workers = [spawn(self._fetch,timeout) for i in xrange(num)]
		gevent.sleep(1)
		
		joinall(self.workers)
		
		

	#fix me
	def stop(self):
		with open("todolog.txt",'a+') as log:
			lst = [item for item in self.todolst.copy()]
			json.dump(lst, log)
		sleep(1)	
			
		gevent.killall(self.workers)
		#for wk in self.workers:
		#	wk.kill(Empty,timeout=1)	
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
	urls =['/question/23556884','/question/19861840','/question/20250938']

	RDB = Redis(db=1)
	#spider = Spider(route, RDB)
	spider = Spider(route,RDB)
	for item in urls:
		spider.put(item)
	try:
		spider.go(10)
	except KeyboardInterrupt, e:
		spider.stop()
	
	
			







