# -*- coding:utf-8 -*-

import unicodedata

from ...configuration import config
from sqlalchemy.sql import text
from .. import utils

def getAllReseaux(connection,public_cible='NAT'):
    sql = """
        SELECT r.id_reseau, code_reseau, nom,picto FROM pn_reseaux.reseaux r
        JOIN pn_reseaux.cor_reseau_public rp ON rp.id_reseau=r.id_reseau
         """
    if(public_cible):
        sql+="WHERE rp.id_nomenclature_type_public=ref_nomenclatures.get_id_nomenclature('TYPE_PUBLIC',:thisPublic)"
    req = connection.execute(text(sql),thisPublic=public_cible)
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
