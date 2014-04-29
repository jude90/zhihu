#coding:utf-8
#from spider import Spider, Handler, Route
import requests
import re
from redis import Redis
from crawler import Crawler, Route, Handler

PEOPLE = "/people/[\w-]+"
QUESTION = "/question/\d+"
SITE = "http://www.zhihu.com"
HEAD = { "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",  
        "Accept": "text/plain"}
route = Route()


@route(PEOPLE)
class People(Handler):
	
	"""docstring for People"""
	def __init__(self, url):
		super(People, self).__init__(url)
		
	def get(self):
		
		page = requests.get(SITE + self.url,headers=HEAD)
		print page.status_code 
		print "got url %s !" %self.url
		return set(re.findall(PEOPLE, page.content)+re.findall(QUESTION, page.content))

@route(QUESTION)
class Question(Handler):
	
	"""docstring for People"""
	def __init__(self, url):
		super(Question, self).__init__(url)
		
	def get(self):
		page = requests.get(SITE +self.url,headers=HEAD)
		print page.status_code 
		print "got url %s !" %self.url
		return set(re.findall(PEOPLE, page.content)+re.findall(QUESTION, page.content))

if __name__ == '__main__':
	RDB = Redis(db=1)
	
	
#	spider = Spider(route, RDB)
#	spider.put("/question/23447870")
#	spider.go(10)
	urls =['/people/xu-chi-45','/question/20664147','/question/21441534','/people/fengduan']

	#spider = Spider(route, RDB)
	cola = Crawler(route,RDB)
	for item in urls:
		cola.put(item)
	cola.go(6)
