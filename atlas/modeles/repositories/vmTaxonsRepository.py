
# -*- coding:utf-8 -*-

from flask import current_app

import unicodedata

from sqlalchemy.sql import text
from .. import utils



# With distinct the result in a array not an object, 0: lb_nom, 1: nom_vern
def getTaxonsCommunes(connection, insee,species_only=False,public_cible='NAT'):
    sql = """
            SELECT 
	            cd_ref_sp as cd_ref,max(date_part('year'::text, o.dateobs)) as last_obs, min(date_part('year'::text, o.dateobs)) as first_obs,
                COUNT(o.id_observation) AS nb_obs, t.nom_complet_html, t.nom_vern, t.lb_nom, t.classe, t.ordre, t.famille,
                t.group2_inpn, t.patrimonial, t.protection_stricte,  bool_or(t.protected) AS protected ,t.code_lr,t.sort_lr, t.sensible,
                coalesce(rnat.code_reseau,'autre') as code_reseau_nat, rnat.picto as picto_reseau_nat, rnat.url as url_reseau_nat, coalesce(rgp.code_reseau,'autre') as code_reseau_gp,rgp.picto as picto_reseau_gp
            FROM atlas.vm_observations o
            JOIN taxonomie.vm_cd_ref_sp ON taxonomie.vm_cd_ref_sp.cd_nom = o.cd_ref
            JOIN atlas.vm_taxons t ON t.cd_ref=cd_ref_sp
            LEFT JOIN pn_reseaux.reseaux rnat ON rnat.id_reseau = t.id_reseau_nat
            LEFT JOIN pn_reseaux.reseaux rgp ON rgp.id_reseau = t.id_reseau_gp
            WHERE o.insee = :thisInsee AND t.id_rang IN ('ES','SSES')
            GROUP BY cd_ref_sp, t.nom_vern, t.nom_complet_html, t.lb_nom, t.classe, t.ordre, t.famille, t.group2_inpn,
                t.patrimonial, t.protection_stricte, rgp.picto, rgp.code_reseau, rnat.picto,  rnat.url, rnat.code_reseau, t.code_lr, t.sort_lr, t.sensible
            ORDER BY nb_obs DESC    
    """
    req = connection.execute(text(sql), thisInsee=insee, publicCible=public_cible)
    taxonCommunesList = list()
    nbObsTotal = 0
    for r in req:
        temp = {
            'nom_complet_html': r.nom_complet_html,
            'lb_nom':r.lb_nom,
            'classe':r.classe,
            'ordre':r.ordre,
            'famille':r.famille,
            'nb_obs': r.nb_obs,
            'nom_vern': r.nom_vern,
            'cd_ref': r.cd_ref,
            'first_obs': int(r.first_obs),
            'last_obs': int(r.last_obs),
            'group2_inpn': utils.deleteAccent(r.group2_inpn),
            'patrimonial': r.patrimonial,
            'protection_stricte': r.protection_stricte,
            'code_reseau_nat':r.code_reseau_nat,
            'code_reseau_gp':r.code_reseau_gp,
            'picto_reseau_nat':r.picto_reseau_nat,
            'url_reseau_nat':r.url_reseau_nat,
            'picto_reseau_gp':r.picto_reseau_gp,
            'protected':r.protected,
            'code_lr':r.code_lr or list(),
            'sort_lr':r.sort_lr or list(),
            'sensible':r.sensible or False,
            'threatened': len(set(('CR','CR*','EN','VU')).intersection(r.code_lr or list()))
        }
        taxonCommunesList.append(temp)
        nbObsTotal = nbObsTotal + r.nb_obs
    return {'taxons': taxonCommunesList, 'nbObsTotal': nbObsTotal}

def getTaxonsTerritory(connection, area_code):
    sql = """
            SELECT 
	            tx.cd_nom as cd_ref,
                max(date_part('year'::text, o.dateobs)) as last_obs, 
                min(date_part('year'::text, o.dateobs)) as first_obs,
                COUNT(o.id_observation) AS nb_obs, 
                tx.nom_complet_html, min(t.nom_vern) as nom_vern, tx.lb_nom, tx.classe, tx.ordre, tx.famille,
                min(COALESCE(gt1.libel,'Autre')) AS grp1,
                min(gt1.picto) as grp1_picto,
                min(COALESCE(gt2.libel,'Autre'))  AS grp2,
                min(gt2.picto) as grp2_picto
            FROM atlas.vm_observations o
            JOIN taxonomie.taxref tx ON tx.cd_nom=taxonomie.find_cdref_sp(o.cd_ref)
            JOIN atlas.vm_taxons2 t ON t.cd_ref=tx.cd_nom
            JOIN atlas.vm_cor_observations_territories cot ON cot.id_observation=o.id_observation
            JOIN atlas.vm_territories ter ON ter.id_area=cot.id_area
            LEFT JOIN atlas.groupes_taxons gt1 ON gt1.id=t.id_grp1
            LEFT JOIN atlas.groupes_taxons gt2 ON gt2.id=t.id_grp2
            WHERE ter.area_code = :thisAreaCode AND t.id_rang IN ('ES','SSES')
            GROUP BY tx.cd_nom
    """
    req = connection.execute(text(sql), thisAreaCode=area_code)
    taxonList = [ dict(r ) for r in req  ]
    return taxonList

def getTaxonsChildsList(connection, cd_ref):
    sql = """
        SELECT DISTINCT nom_complet_html, coalesce(nb_obs,0) as nb_obs, nom_vern, tax.cd_ref,
            yearmax, group2_inpn, patrimonial, protection_stricte,
            chemin, url, m.id_media
        FROM atlas.vm_taxons tax
        JOIN atlas.bib_taxref_rangs bib_rang
        ON trim(tax.id_rang)= trim(bib_rang.id_rang)
        LEFT JOIN atlas.vm_medias m
        ON m.cd_ref = tax.cd_ref AND m.id_type={}
        WHERE tax.cd_ref IN (
            SELECT * FROM atlas.find_all_taxons_childs(:thiscdref)
        ) """.format(str(current_app.config['ATTR_MAIN_PHOTO']))
    req = connection.execute(text(sql), thiscdref=cd_ref)
    taxonRankList = list()
    nbObsTotal = 0
    for r in req:
        temp = {
            'nom_complet_html': r.nom_complet_html,
            'nb_obs': r.nb_obs,
            'nom_vern': r.nom_vern,
            'cd_ref': r.cd_ref,
            'last_obs': r.yearmax,
            'group2_inpn': utils.deleteAccent(r.group2_inpn),
            'patrimonial': r.patrimonial,
            'protection_stricte': r.protection_stricte,
            'path': utils.findPath(r),
            'id_media': r.id_media
        }
        taxonRankList.append(temp)
        nbObsTotal = nbObsTotal + r.nb_obs
    return {'taxons': taxonRankList, 'nbObsTotal': nbObsTotal}


def getINPNgroupPhotos(connection):
    """
        Get list of INPN groups with at least one photo
    """

    sql = """
        SELECT DISTINCT count(*) AS nb_photos, group2_inpn
        FROM atlas.vm_taxons T
        JOIN atlas.vm_medias M on M.cd_ref = T.cd_ref
        GROUP BY group2_inpn
        ORDER BY nb_photos DESC
    """
    req = connection.execute(text(sql))
    groupList = list()
    for r in req:
        temp = {
            'group': utils.deleteAccent(r.group2_inpn),
            'groupAccent': r.group2_inpn
        }
        groupList.append(temp)
    return groupList


def getTaxonsGroup(connection, groupe):
    sql = """
        SELECT t.cd_ref, t.nom_complet_html, t.nom_vern, t.nb_obs,
            t.group2_inpn, t.protection_stricte, t.patrimonial, t.yearmax,
            m.chemin, m.url, m.id_media,
            t.nb_obs
        FROM atlas.vm_taxons t
        LEFT JOIN atlas.vm_medias m
        ON m.cd_ref = t.cd_ref AND m.id_type={}
        WHERE t.group2_inpn = :thisGroupe
        GROUP BY t.cd_ref, t.nom_complet_html, t.nom_vern, t.nb_obs,
            t.group2_inpn, t.protection_stricte, t.patrimonial, t.yearmax,
            m.chemin, m.url, m.id_media
        """.format(current_app.config['ATTR_MAIN_PHOTO'])
    req = connection.execute(text(sql), thisGroupe=groupe)
    tabTaxons = list()
    nbObsTotal = 0
    for r in req:
        nbObsTotal = nbObsTotal+r.nb_obs
        temp = {
            'nom_complet_html': r.nom_complet_html,
            'nb_obs': r.nb_obs,
            'nom_vern': r.nom_vern,
            'cd_ref': r.cd_ref,
            'last_obs': r.yearmax,
            'group2_inpn': utils.deleteAccent(r.group2_inpn),
            'patrimonial': r.patrimonial,
            'protection_stricte': r.protection_stricte,
            'id_media': r.id_media,
            'path': utils.findPath(r)
        }
        tabTaxons.append(temp)
    return {'taxons': tabTaxons, 'nbObsTotal': nbObsTotal}


# get all groupINPN
def getAllINPNgroup(connection):
    sql = """
        SELECT SUM(nb_obs) AS som_obs, group2_inpn
        FROM atlas.vm_taxons
        GROUP BY group2_inpn
        ORDER by som_obs DESC
    """
    req = connection.execute(text(sql))
    groupList = list()
    for r in req:
        temp = {
            'group': utils.deleteAccent(r.group2_inpn),
            'groupAccent': r.group2_inpn
        }
        groupList.append(temp)
    return groupList
