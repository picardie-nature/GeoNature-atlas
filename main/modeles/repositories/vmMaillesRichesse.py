# -*- coding:utf-8 -*-

from .. import utils
from sqlalchemy.sql import text
import ast

def getAtlasReseau(connection,id_liste, type_maille='l93_5'):
    """
    Retourne les data pour les cartes de richesses specifique et occurences par maille
    """
    sql = """SELECT
	        id_maille, id_liste, n_sp,n_occ, st_asgeojson(st_transform(the_geom,4326)) as geojson_maille
        FROM atlas.vm_atlas_thematique
        WHERE id_liste=(:thisidliste)
        """
    
    data = connection.execute(text(sql), thisidliste=id_liste)
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
