import import_clicnat as imp
import psycopg2
from sys import argv
from config import Hyla, Aves, GnAtlas, GeoNature

db=Hyla()

conn = psycopg2.connect(db.url)
cur = conn.cursor()

from_year = argv[1]
to_year = argv[2]

try:
    classe_filter = argv[3]
except IndexError:
    classe_filter = None

q = 'SELECT DISTINCT taxref_inpn_especes,id_espece FROM especes WHERE taxref_inpn_especes IS NOT NULL'
if classe_filter :
    q+=" AND classe ='{}'".format(classe_filter)

#print(cur.mogrify(q))
cur.execute(q)

for e in cur :
    imp.import_obs(e[1],from_year,to_year)
    print('Imported {} ({} to {})'.format(e[1],from_year,to_year))


#Pour les fiches communes :
"""
UPDATE synthese.syntheseff SET
insee = atlas.l_communes.insee
FROM atlas.l_communes
WHERE 
	syntheseff.insee is NULL
	AND st_contains(atlas.l_communes.the_geom,synthese.syntheseff.the_geom_point)
"""