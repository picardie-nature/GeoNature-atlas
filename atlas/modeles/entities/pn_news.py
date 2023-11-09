from sqlalchemy import Column, Integer, MetaData, String, Table, Float, DateTime, ARRAY
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base
from ...utils import engine


Base = declarative_base()
metadata = MetaData()

class Feed(Base):
    __table__ = Table(
    'pn_work_feed', metadata,
    Column('id_item', Integer, primary_key=True, unique=True),
    Column('source', String()),
    Column('guid', String()),
    Column('title', String()),
    Column('link', String()),
    Column('description', String()),
    Column('pubdate', DateTime()),
    Column('keywords', ARRAY(String)),
    Column('authors', ARRAY(String)),  
    schema='pn_work_news', autoload=True, autoload_with=engine
)
