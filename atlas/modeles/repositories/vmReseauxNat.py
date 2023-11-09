# -*- coding:utf-8 -*-

import unicodedata

from ...configuration import config
from sqlalchemy.sql import text
from .. import utils

def getAllReseaux(connection,grand_public=False):
    sql = """
        SELECT s.id_subset, s.id_subset::text, s.nom, s.picto FROM pn_custom_taxonomie.pn_custom_subset s
         """
    if(grand_public):
        sql+="WHERE s.niveau_subset = 0"
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
