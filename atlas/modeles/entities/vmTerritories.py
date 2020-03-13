# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, Integer, MetaData, String, Table, Text
from geoalchemy2.types import Geometry
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base
from ...utils import engine

metadata = MetaData()
Base = declarative_base()

class VmTerritories(Base):
    __table__ = Table(
    'vm_territories', metadata,
    Column('id_area', Integer,primary_key=True, unique=True),
    Column('area_code', String(25)),
    Column('area_name', String(250)),
    Column('area_type', String(25)),
    Column('geom', Geometry(u'MULTIPOLYGON', 3157), index=True),
    schema='atlas', autoload=True, autoload_with=engine
)
