# -*- coding:utf-8 -*-

from sqlalchemy.sql import text


def getTerritorieFromCode(connection, area_code):
    sql="SELECT * FROM atlas.vm_territories WHERE area_code=:thisAreaCode LIMIT 1"
    req = connection.execute(text(sql), thisAreaCode=area_code)
    return dict(req.fetchone().items())

