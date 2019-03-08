from sys import argv
import psycopg2
#from config import PASSWORD, PASSWORD_ATLAS, HOST
from config import Hyla, Aves, GnAtlas, GeoNature

#a mettre en parametre
#id_espece = argv[1]
#from_year = argv[2]
#to_year = argv[3]


#TODO recuperer aussi les obs des autres espaces + traitement des polygones (cf commission des reseaux)
query="""
WITH cit_filter AS (
	SELECT c.id_citation from citations c
	JOIN observations o ON c.id_observation=o.id_observation
	JOIN citations_tags ct ON ct.id_citation=c.id_citation
	JOIN tags t ON ct.id_tag=t.id_tag
	WHERE 
		t.ref='INV!'
		OR o.brouillard=True
	
	)
SELECT e.taxref_inpn_especes as cd_nom,o.date_observation as date,
string_agg(u.prenom ||' ' || upper(u.nom),', ') AS observateurs,
ST_AsEWKT(st_transform(coalesce(point.the_geom,chiro.the_geom),3857)) as geom
FROM citations c
JOIN observations o ON o.id_observation = c.id_observation
JOIN especes e ON e.id_espece = c.id_espece
JOIN observations_observateurs oo ON oo.id_observation = o.id_observation
JOIN utilisateur u ON u.id_utilisateur = oo.id_utilisateur
LEFT JOIN espace_point point ON o.espace_table='espace_point' AND o.id_espace=point.id_espace
LEFT JOIN espace_chiro chiro ON o.espace_table='espace_chiro' AND o.id_espace=chiro.id_espace
WHERE c.id_citation NOT IN (SELECT id_citation FROM cit_filter) AND
e.id_espece=%s AND
date_part('year',o.date_observation) >= %s AND date_part('year',o.date_observation) <= %s
GROUP BY cd_nom, date,geom
"""

#######
#     #
# DB  #
#     #
#######
db=Hyla()
db_atlas=GeoNature()

def import_obs(id_espece,from_year,to_year):
    conn = psycopg2.connect(db.url)
    cur = conn.cursor()
    conn_atlas = psycopg2.connect(db_atlas.url)
    cur_atlas = conn_atlas.cursor()
    cur.execute(query,(id_espece,from_year,to_year))
    #TODO voir pour inserer plusieurs enregistrement dans un INSERT
    i=0
    for r in cur:
        i+=1
        q="""INSERT INTO synthese.syntheseff(cd_nom,dateobs,observateurs,altitude_retenue,supprime,the_geom_point,effectif_total,diffusable) 
            VALUES ({},'{}','{}',0,False,ST_GeomFromEWKT('{}'),1,True);
            """.format(*r)

        q="""INSERT INTO synthese.syntheseff(cd_nom,dateobs,observateurs,altitude_retenue,supprime,the_geom_point,effectif_total,diffusable) 
            VALUES (%s,%s,%s,0,False,ST_GeomFromEWKT(%s),1,True);
            """
        try :
            cur_atlas.execute(q,(r))
        except :
            pass
        if i%1000 == 0:
            conn_atlas.commit()
            print(i)
        #print(q)
    print(i)
    conn_atlas.commit()
    cur.close()
    conn.close()
    cur_atlas.close()
    conn_atlas.close()
