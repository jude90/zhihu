#coding:utf-8
import gevent.monkey
gevent.monkey.patch_all()
from gevent.queue import Empty, Queue
import gevent
import requests
from urlparse import urlparse, parse_qs
import re

class Spider(object):
	"""docstring for Spider"""
	def __init__(self, route, RDB):
		
		self.route = route
		self.visited = RDB
		self.todolst = Queue()

