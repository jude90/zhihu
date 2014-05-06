#coding:utf-8
#from spider import Spider, Handler, Route
import requests
import re
from redis import Redis
from crawler import Crawler, Route, Handler
from model import  DB_Session, User
from lxml import etree 

PEOPLE = "/people/[\w-]+"
QUESTION = "/question/\d+"
SITE = "http://www.zhihu.com"
HEAD = { "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",  
        "Accept": "text/plain"}
route = Route()


@route(PEOPLE)
class People(Handler):
	session = DB_Session()
	"""docstring for People"""
	def __init__(self, url):
		super(People, self).__init__(url)
		
	def get(self):
		
		page = requests.get(SITE + self.url,headers=HEAD)
		dom = etree.HTML(page.content)
		session = DB_Session()
		# ugly code
		people = {}
		people['name'] = self.url
		people['bio']  = (dom.xpath("//span[@class='bio']/@title") or " ")[0].encode("utf-8")
		people['location'] = (dom.xpath("//span[@class='location item']/@title") or " ")[0].encode("utf-8")
		people['business'] = (dom.xpath("//span[@class='business item']/@title") or " ")[0].encode("utf-8")
		people['education'] = (dom.xpath("//span[@class='education item']/@title") or " ")[0].encode("utf-8")
		session.execute(User.__table__.insert(), people)
		session.commit()
		session.close()
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
	urls =['/question/20055305','/question/20664147','/question/21441534','/people/fengduan']

	#spider = Spider(route, RDB)
	cola = Crawler(route,RDB)
	
	for i in xrange(50):
		key = RDB.randomkey()
		if RDB.get(key) =="todo":
			cola.put(key)	
	cola.go(10)



