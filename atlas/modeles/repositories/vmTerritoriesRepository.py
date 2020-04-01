# -*- coding:utf-8 -*-

from sqlalchemy.sql import text


def getTerritorieFromCode(connection, area_code):
    sql="SELECT * FROM atlas.vm_territories WHERE area_code=:thisAreaCode LIMIT 1"
    req = connection.execute(text(sql), thisAreaCode=area_code)
    return dict(req.fetchone().items())


def getTerritorieKnoweldgeEvolution(connection, area_code):
    sql="""SELECT n_taxon, n_occurence, n_observer, date_part('year', t) AS "year"
        FROM atlas.vm_territories_knoweldge_evolution tke
        JOIN atlas.vm_territories t ON t.id_area =tke.id_area WHERE area_code=:thisAreaCode ORDER BY t;"""
    req = connection.execute(text(sql), thisAreaCode=area_code)
    return [ dict(r) for r in req  ]


def getTerritoriesSearch(connection, search, limit=50):
    sql = "SELECT area_name, area_code, area_type  FROM atlas.vm_territories WHERE area_name ILIKE :thisSearch ORDER BY char_length(area_name) LIMIT :thisLimit"
    req = connection.execute(text(sql), thisSearch='%{}%'.format(search), thisLimit=limit)
    TerritoriesList = list()
    for r in req:
        temp = {'label': r[0], 'value': r[1], 'type':r[2]}
        TerritoriesList.append(temp)
    return TerritoriesList
