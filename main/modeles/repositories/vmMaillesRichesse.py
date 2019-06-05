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

def getEspecesMaille(connection, id_maille, id_liste):
    sql = """
        SELECT DISTINCT bib_noms.cd_ref AS cd_nom, COALESCE(bib_noms.nom_francais,taxref.nom_vern) as nom_vern, taxref.lb_nom
        FROM atlas.vm_observations_mailles vm_observations_mailles
        JOIN taxonomie.bib_noms bib_noms ON bib_noms.cd_ref = vm_observations_mailles.cd_ref
        JOIN taxonomie.taxref taxref ON taxref.cd_nom = vm_observations_mailles.cd_ref
        JOIN taxonomie.cor_nom_liste liste ON liste.id_nom=bib_noms.id_nom
        WHERE taxref.id_rang='ES' and id_maille=(:thisidmaille) and liste.id_liste = (:thisidliste)
        ORDER BY lb_nom"""
    data = connection.execute(text(sql), thisidmaille=id_maille,thisidliste=id_liste )
    tab=list()
    for e in data:
        tab.append({
            'properties':{
                'cd_nom':e.cd_nom,
                'nom_vern':e.nom_vern,
                'lb_nom':e.lb_nom
            },
            'type' : "Feature"
        })
    outGeoJson={'type':"FeatureCollection", 'features':tab}
    return outGeoJson
