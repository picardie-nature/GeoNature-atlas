import import_clicnat as imp
import psycopg2
from sys import argv
from config import PASSWORD, PASSWORD_ATLAS, HOST

conn = psycopg2.connect(dbname="clicnat", user="jb", host=HOST, password=PASSWORD)
cur = conn.cursor()

from_year = argv[1]
to_year = argv[2]


cur.execute('SELECT DISTINCT taxref_inpn_especes,id_espece FROM especes WHERE taxref_inpn_especes IS NOT NULL')

for e in cur :
    imp.import_obs(e[1],from_year,to_year)
    print('Imported {} ({} to {})'.format(e[1],from_year,to_year))
