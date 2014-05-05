from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Unicode

from sqlalchemy.ext.declarative import declarative_base

DB_CONNECT_STRING ='mysql+mysqldb://root:@localhost/zhihu?charset=utf8'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind= engine)
session = DB_Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'peoples';
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255,convert_unicode=False))
    bio = Column(Unicode(255,convert_unicode=False))
    
    business = Column(Unicode(255,convert_unicode=False))
    location = Column(Unicode(255,convert_unicode=False))
    education = Column(Unicode(255,convert_unicode=False))

if __name__ == '__main__':
    Base.metadata.create_all(engine)