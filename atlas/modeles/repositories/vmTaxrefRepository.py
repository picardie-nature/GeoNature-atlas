
# -*- coding:utf-8 -*-
from flask import current_app
from .. import utils
from ..entities.vmTaxref import VmTaxref
from ..entities.tBibTaxrefRang import TBibTaxrefRang
from sqlalchemy.sql import text


def searchEspece(connection, cd_ref):
    """
        recherche l espece corespondant au cd_nom et tout ces fils
    """
    sql = """
    WITH limit_obs AS (
        select
            :thiscdref as cd_ref, min(yearmin) AS yearmin,
            max(yearmax) AS yearmax, SUM(nb_obs) AS nb_obs
        FROM atlas.vm_taxons
        WHERE
            cd_ref in (SELECT * FROM atlas.find_all_taxons_childs(:thiscdref))
            OR cd_ref = :thiscdref
    )
    SELECT taxref.*, l.*, t2.patrimonial, t2.protection_stricte, t2.code_lr, t22.rarete, t2.protected, t2.sensible, t2.eee, doc_lr.full_citation as doc_lr_citation,doc_lr.doc_url as doc_lr_url,
            coalesce(rnat.code_reseau,'autre') as code_reseau_nat, rnat.picto as picto_reseau_nat, rnat.url as url_reseau_nat, coalesce(rgp.code_reseau,'autre') as code_reseau_gp,rgp.picto as picto_reseau_gp
    FROM atlas.vm_taxref taxref
    JOIN limit_obs l ON l.cd_ref = taxref.cd_nom
    LEFT JOIN atlas.vm_taxons t2 ON t2.cd_ref = taxref.cd_ref
    LEFT JOIN atlas.vm_taxons2 t22 ON t22.cd_ref = taxref.cd_ref
    LEFT JOIN taxonomie.bdc_statuts_doc doc_lr ON doc_lr.cd_doc=t2.cd_doc_lr
    LEFT JOIN pn_reseaux.reseaux rnat ON rnat.id_reseau = t2.id_reseau_nat
    LEFT JOIN pn_reseaux.reseaux rgp ON rgp.id_reseau = t2.id_reseau_gp
    WHERE taxref.cd_nom = :thiscdref
    """
    req = connection.execute(text(sql), thiscdref=cd_ref)
    taxonSearch = dict()
    for r in req:
        taxonSearch = {
            'cd_ref': r.cd_ref,
            'lb_nom': r.lb_nom,
            'nom_vern': r.nom_vern,
            'lb_auteur': r.lb_auteur,
            'nom_complet_html': r.nom_complet_html,
            'group2_inpn': utils.deleteAccent(r.group2_inpn),
            'groupAccent': r.group2_inpn,
            'yearmin': r.yearmin,
            'yearmax': r.yearmax,
            'nb_obs': r.nb_obs,
            'patrimonial': r.patrimonial,
            'protection': r.protection_stricte,
            'liste_rouge':r.code_lr or list(),
            'rarete':r.rarete,
            'protected':r.protected,
            'eee':r.eee,
            'code_reseau_nat':r.code_reseau_nat,
            'code_reseau_gp':r.code_reseau_gp,
            'picto_reseau_nat':r.picto_reseau_nat,
            'url_reseau_nat':r.url_reseau_nat,
            'picto_reseau_gp':r.picto_reseau_gp,
            'sensible':r.sensible,
            'doc_lr_citation':r.doc_lr_citation,
            'doc_lr_url':r.doc_lr_url
        }

    sql = """
        SELECT
            tax.lb_nom,
            tax.nom_vern,
            tax.cd_ref,
            br.tri_rang,
            tax.group2_inpn,
            tax.patrimonial,
            tax.protection_stricte,
            tax.nb_obs
        FROM atlas.vm_taxons tax
        JOIN atlas.bib_taxref_rangs br
        ON br.id_rang = tax.id_rang
        WHERE tax.cd_ref IN (
            SELECT * FROM atlas.find_all_taxons_childs(:thiscdref)
        )
    """
    req = connection.execute(text(sql), thiscdref=cd_ref)
    listTaxonsChild = list()
    for r in req:
        temp = {
            'lb_nom': r.lb_nom,
            'nom_vern': r.nom_vern,
            'cd_ref': r.cd_ref,
            'tri_rang': r.tri_rang,
            'group2_inpn': utils.deleteAccent(r.group2_inpn),
            'patrimonial': r.patrimonial,
            'nb_obs': r.nb_obs,
            'protection': r.protection_stricte
        }
        listTaxonsChild.append(temp)

    return {
        'taxonSearch': taxonSearch,
        'listTaxonsChild': listTaxonsChild
    }


def getSynonymy(connection, cd_ref):
    sql = """
        SELECT nom_complet_html, lb_nom
        FROM atlas.vm_taxref
        WHERE cd_ref = :thiscdref
        ORDER BY lb_nom ASC
    """
    req = connection.execute(text(sql), thiscdref=cd_ref)
    tabSyn = list()
    for r in req:
        temp = {'lb_nom': r.lb_nom, 'nom_complet_html': r.nom_complet_html}
        tabSyn.append(temp)
    return tabSyn


def getTaxon(session, cd_nom):
    req = session.query(
        VmTaxref.lb_nom, VmTaxref.id_rang, VmTaxref.cd_ref,
        VmTaxref.cd_taxsup, TBibTaxrefRang.nom_rang, TBibTaxrefRang.tri_rang
    ).join(
        TBibTaxrefRang, TBibTaxrefRang.id_rang == VmTaxref.id_rang
    ).filter(VmTaxref.cd_nom == cd_nom)
    return req[0]


def getCd_sup(session, cd_ref):
    req = session.query(VmTaxref.cd_taxsup).filter(VmTaxref.cd_nom == cd_ref).first()
    return req.cd_taxsup


def getInfoFromCd_ref(session, cd_ref):
    req = session.query(
        VmTaxref.lb_nom, TBibTaxrefRang.nom_rang
    ).join(
        TBibTaxrefRang, TBibTaxrefRang.id_rang == VmTaxref.id_rang
    ).filter(VmTaxref.cd_ref == cd_ref)

    return {'lb_nom': req[0].lb_nom, 'nom_rang': req[0].nom_rang}


def getAllTaxonomy(session, cd_ref):
    taxonSup = getCd_sup(session, cd_ref)  # cd_taxsup
    taxon = getTaxon(session, taxonSup)
    tabTaxon = list()
    while taxon.tri_rang >= current_app.config['LIMIT_RANG_TAXONOMIQUE_HIERARCHIE']:
        temp = {
            'rang': taxon.id_rang,
            'lb_nom': taxon.lb_nom,
            'cd_ref': taxon.cd_ref,
            'nom_rang': taxon.nom_rang,
            'tri_rang': taxon.tri_rang
        }
        tabTaxon.insert(0, temp)
        taxon = getTaxon(session, taxon.cd_taxsup)  # on avance
    return tabTaxon
