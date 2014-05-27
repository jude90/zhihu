#
from bottle import * 
from redis import StrictRedis
import sys
sys.path.append("..")
from model import  DB_Session, User

Session = DB_Session()
query = Session.query(User)
urlprefix =""
rdb = StrictRedis(db=2)

@route("%s/" %urlprefix)
def index():
	return template("index.html")



@route("%s/name"%urlprefix)
def find_people():
	key = request.GET.get('keyword')
	#return str(request.GET.get
	if key:
		userlst = rdb.smembers(key)
   		users = { user : Session.execute("SELECT bio FROM peoples WHERE name='{0}'".format(user)).fetchall()[0][0].encode("utf-8") for user in userlst}
   		return template("result.tpl",peoples= users)
	else:
		redirect("%s/"%urlprefix)



debug(True)

run(host="127.0.0.1", port=8080,reloader=True)
