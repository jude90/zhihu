#
from bottle import * 
from redis import StrictRedis
import sys
sys.path.append("..")
from model import  DB_Session, User


urlprefix =""
rdb = StrictRedis(db=2)

@route("%s/" %urlprefix)
def index():
	return template("index.html")



@route("%s/name"%urlprefix)
def find_people():
	key = request.GET.get('keyword')
	#return str(request.GET.get
	if key :
		userlst = rdb.smembers(key)
		return template("result.tpl",
						peoples= userlst)
	else:
		redirect("%s/"%urlprefix)





























debug(True)

run(host="127.0.0.1", port=8080,reloader=True)
