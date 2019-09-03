
# -*- coding:utf-8 -*-

import ast
from ..entities.vmCommunes import VmCommunes
from sqlalchemy import distinct
from sqlalchemy.sql import text


def getAllCommunes(session):
    req = session.query(distinct(VmCommunes.commune_maj), VmCommunes.insee).all()
    communeList = list()
    for r in req:
        temp = {'label': r[0], 'value': r[1]}
        communeList.append(temp)
    return communeList


def getCommunesSearch(connection, search, limit=50):
    sql = "SELECT commune_maj, insee  FROM atlas.vm_communes WHERE commune_maj ILIKE :thisSearch ORDER BY char_length(commune_maj) LIMIT :thisLimit"
    req = connection.execute(text(sql), thisSearch='%{}%'.format(search), thisLimit=limit)
    communeList = list()
    for r in req:
        temp = {'label': r[0], 'value': r[1]}
        communeList.append(temp)
    return communeList


def getCommuneFromInsee(connection, insee):
    sql = """SELECT c.commune_maj, 
           c.insee, 
           c.commune_geojson, 
           c.image_url,
           c.image_credit
           FROM atlas.vm_communes c 
           WHERE c.insee = :thisInsee"""
    req = connection.execute(text(sql), thisInsee=insee)
    communeObj = dict()
    for r in req:
        communeObj = {
            'communeName': r.commune_maj,
            'insee': str(r.insee),
            'communeGeoJson': ast.literal_eval(r.commune_geojson),
            'image_url' : r.image_url or None,
            'image_credit' : r.image_credit or None
        }
    return communeObj

    return req[0].commune_maj


def getCommunesObservationsChilds(connection, cd_ref):
    sql = """
    SELECT DISTINCT (com.insee) as insee, com.commune_maj, count(id_observation) AS n_obs, max(dateobs) AS last_obs, min(dateobs) AS first_obs
    FROM atlas.vm_communes com
    JOIN atlas.vm_observations obs
    ON obs.insee = com.insee
    WHERE obs.cd_ref in (
            SELECT * from atlas.find_all_taxons_childs(:thiscdref) UNION SELECT :thiscdref
        )
    GROUP BY com.insee,com.commune_maj
    ORDER BY com.commune_maj ASC
    """
    req = connection.execute(text(sql), thiscdref=cd_ref)
    listCommunes = list()
    for r in req:
        temp = {'insee': r.insee, 'commune_maj': r.commune_maj,'first_obs':r.first_obs,'last_obs':r.last_obs,'n_obs':r.n_obs}
        listCommunes.append(temp)
    return listCommunes
