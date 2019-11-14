
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from .configuration.config import database_connection,NOM_APPLICATION
from sqlalchemy.pool import QueuePool
from sqlalchemy.sql import text
engine = create_engine(database_connection, client_encoding='utf8', echo = False, poolclass=QueuePool,  connect_args={"application_name":"GN-atlas_{}".format(NOM_APPLICATION)} )


def loadSession():
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def format_number(val):
    """ Ajouter des espaces en séparateur de milliers """
    if not val :
        return '-'
    return format(int(val),',d').replace(',',' ')

def idtier2cdref(id_tiers,tiers):
    session = loadSession()
    connection = engine.connect()
    sql = """
        SELECT taxonomie.find_cdref(cd_nom) as cd_ref FROM taxonomie.ref_tiers 
        WHERE id_tiers=:id_tiers AND tiers=:tiers
        LIMIT 1
        """
    req = connection.execute(text(sql), id_tiers=id_tiers, tiers=tiers)
    r = req.first()
    connection.close()
    session.close()
    if not r :
        return None
    return r['cd_ref']

def idtier2areacode(id_tiers,tiers):
    session = loadSession()
    connection = engine.connect()
    sql = """
        SELECT area_code FROM ref_geo.ref_tiers 
        WHERE id_tiers=:id_tiers AND tiers=:tiers
        LIMIT 1
        """
    req = connection.execute(text(sql), id_tiers=id_tiers, tiers=tiers)
    r = req.first()
    connection.close()
    session.close()
    if not r :
        return None
    return r['area_code']
