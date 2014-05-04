from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

DB_CONNECT_STRING ='mysql+mysqldb://root:@localhost/zhihu?charset=utf8'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind= engine)
session = DB_Session()
Base = declarative_base()

class People(Base):
    __tablename__ = 'peoples';
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    bio = Column(String(255))
    
    employ = Column(String(255))
    location = Column(String(255))
    education = Column(String(255))

if __name__ == '__main__':
    Base.metadata.create_all(engine)