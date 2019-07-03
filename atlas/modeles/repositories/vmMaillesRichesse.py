# -*- coding:utf-8 -*-

from .. import utils
from sqlalchemy.sql import text
import ast

def getAtlasReseau(connection,id_liste, type_maille='l93_5'):
    """
    Retourne les data pour les cartes de richesses specifique et occurences par maille
    """
    sql = """
    SELECT om.id_maille,
    cor_nom_liste.id_liste,
    count(DISTINCT 
    		CASE WHEN taxref.id_rang = 'ES' THEN taxref.cd_ref
    			WHEN taxref.id_rang::text = 'SSES' THEN taxref.cd_sup END
    	) AS n_sp,
    count(DISTINCT o.id_observation) AS n_occ,
    st_asgeojson(st_transform(om.the_geom,4326)) as geojson_maille
   FROM atlas.vm_observations o
     JOIN atlas.vm_observations_mailles om ON om.id_observation = o.id_observation
     JOIN taxonomie.bib_noms ON bib_noms.cd_ref = om.cd_ref
     JOIN taxonomie.cor_nom_liste ON cor_nom_liste.id_nom = bib_noms.id_nom
     JOIN taxonomie.taxref ON taxref.cd_nom = om.cd_ref 
     WHERE cor_nom_liste.id_liste=(:thisidliste) AND taxref.id_rang in ('ES','SSES') AND o.date_min >= '2009-01-01 00:00:00'::timestamp without time ZONE 
  GROUP BY om.id_maille, cor_nom_liste.id_liste, om.the_geom
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
        JOIN atlas.vm_observations o ON o.id_observation = vm_observations_mailles.id_observation
        JOIN taxonomie.bib_noms bib_noms ON bib_noms.cd_ref = vm_observations_mailles.cd_ref
        JOIN taxonomie.taxref taxref ON taxref.cd_nom = vm_observations_mailles.cd_ref
        JOIN taxonomie.cor_nom_liste liste ON liste.id_nom=bib_noms.id_nom
        WHERE taxref.id_rang='ES' and id_maille=(:thisidmaille) and liste.id_liste = (:thisidliste) AND o.date_min > '2009-01-01'
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

def getStatLastObsMailles(connection,since=15):
    sql = """
        SELECT id_maille, count(om.id_observation) as n_obs, count(DISTINCT om.cd_ref) as n_taxons, st_asgeojson(st_transform(om.the_geom,4326)) as geojson_maille 
        FROM atlas.vm_observations_mailles om
        JOIN atlas.vm_observations o ON o.id_observation = om.id_observation
        WHERE o.date_min > now() - INTERVAL '{}' DAY
        GROUP BY id_maille, st_asgeojson(st_transform(om.the_geom,4326));
        """.format(since)
    data = connection.execute(text(sql) )
    tab=list()
    for e in data:
        tab.append({
            'properties':{
                'n_obs':e.n_obs,
                'n_taxons':e.n_taxons,
                'id_maille':e.id_maille
            },
            'type' : "Feature",
            'geometry': ast.literal_eval(e.geojson_maille)
        })
    outGeoJson={'type':"FeatureCollection", 'features':tab}
    return outGeoJson

