from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine
from redis import StrictRedis
import re
import jieba


rdb = StrictRedis(db=2)
DB_CONNECT_STRING ='mysql+mysqldb://root:@localhost/zhihu?charset=utf8'
WD = re.compile(ur"^[\u4e00-\u9fa5_a-zA-Z0-9]+$")

engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind= engine)


session = DB_Session()

result = session.execute("select name,bio from peoples where bio !=' '")

for name, bio in result.fetchall():
	[rdb.sadd(word,name) for word in jieba.cut(bio)]

