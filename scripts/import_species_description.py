import psycopg2

from config import Hyla, Aves, GnAtlas


############ CONFIG ################
db = Hyla()
db_atlas = GnAtlas()
DRY_RUN = True
############ END CONFIG ############

conn = psycopg2.connect(db.url)
cur = conn.cursor()

conn_atlas = psycopg2.connect(db_atlas.url)
cur_atlas = conn_atlas.cursor()

query="""SELECT id_espece, taxref_inpn_especes, habitat, menace, action_conservation,commentaire_statut_menace
  FROM especes WHERE habitat is not null AND taxref_inpn_especes is not null"""

cur.execute(query)

for espece in cur: #TODO check cd_ref + autres champs
    if espece[2] is not None: #habitat
        params = (100, espece[2],espece[1])
        query = "INSERT INTO taxonomie.cor_taxon_attribut (id_attribut,valeur_attribut,cd_ref) VALUES (%s,%s,%s)"
        print(cur_atlas.mogrify(query,params))
        try :
            cur_atlas.execute(query,params)
        except psycopg2.IntegrityError :
            conn_atlas.rollback()
            continue
        conn_atlas.commit()

conn_atlas.commit()
cur_atlas.close()
conn_atlas.close()

cur.close()
conn.close()