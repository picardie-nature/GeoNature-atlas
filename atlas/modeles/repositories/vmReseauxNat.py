# -*- coding:utf-8 -*-

import unicodedata

from ...configuration import config
from sqlalchemy.sql import text
from .. import utils

def getAllReseaux(connection):
    sql = """
        SELECT id_reseau, code_reseau, nom,picto  FROM pn_reseaux.reseaux
         """
    req = connection.execute(text(sql))
    reseauxList=list()
    for r in req:
        temp = {
            'id_reseau': r.id_reseau,
            'code_reseau':r.code_reseau,
            'nom_reseau':r.nom,
            'picto_reseau':r.picto
        }
        reseauxList.append(temp)
    return reseauxList
