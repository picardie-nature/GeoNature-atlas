#!/bin/bash
password=$1
host=127.0.0.1
user=geonatadmin
db=geonature2db


#PGPASSWORD=$1 nohup psql -U $user -h $host -f import_foreign.sql -d $db

PGPASSWORD=$1 psql -h $host -w -U $user $db -c "REFRESH MATERIALIZED VIEW atlas.vm_observations"
PGPASSWORD=$1 psql -h $host -w -U $user $db -c "REFRESH MATERIALIZED VIEW atlas.vm_observations_mailles"
PGPASSWORD=$1 psql -h $host -w -U $user $db -c "REFRESH MATERIALIZED VIEW atlas.vm_taxons"
PGPASSWORD=$1 psql -h $host -w -U $user $db -c "REFRESH MATERIALIZED VIEW atlas.vm_taxons_plus_observes"
PGPASSWORD=$1 psql -h $host -w -U $user $db -c "REFRESH MATERIALIZED VIEW atlas.vm_search_taxon"
PGPASSWORD=$1 psql -h $host -w -U $user $db -c "REFRESH MATERIALIZED VIEW atlas.vm_mois"
PGPASSWORD=$1 psql -h $host -w -U $user $db -c "REFRESH MATERIALIZED VIEW atlas.vm_medias"

