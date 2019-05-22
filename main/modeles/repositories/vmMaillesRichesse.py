# -*- coding:utf-8 -*-

from .. import utils
from sqlalchemy.sql import text
import ast

def getAtlasReseau(connection,id_reseau, type_maille='l93_5'):
    """
    Retourne les data pour les cartes de richesses specifique et occurences par maille
    """
    sql = """SELECT
	        id_maille, id_reseau, n_sp,n_occ, st_asgeojson(the_geom) as geojson_maille
        FROM atlas.maille_richesse_sp
        WHERE id_reseau=(:thisidreseau)
        """
    
    data = connection.execute(text(sql), thisidreseau=id_reseau)
    tab=list()
    for e in data:
        tab.append({
            'properties':{
                'id_maille':e.id_maille,
                'n_sp':e.n_sp,
                'n_occ':e.n_occ
            },
            'geometry': ast.literal_eval(e.geojson_maille),
            'type' : "Feature"
            
        })
    outGeoJson={'type':"FeatureCollection", 'features':tab}
    return outGeoJson
