
# -*- coding:utf-8 -*-

from sqlalchemy.sql import text


def getAttributesTaxon(
    connection, cd_ref, attrDesc, attrComment, attrMilieu, attrChoro, attrConnaissance = None, attrHab = None, attrPheno = None, attrPop = None, attrIdentification = None
):
    sql = """
        SELECT *
        FROM atlas.vm_cor_taxon_attribut
        WHERE id_attribut IN (:thisattrDesc, :thisattrComment, :thisattrMilieu, :thisattrChoro, :thisattrConnaissance, :thisattrHab,:thisattrPheno,:thisattrPop,:thisattrIdentif  )
        AND cd_ref = :thiscdref
    """
    req = connection.execute(
        text(sql),
        thiscdref=cd_ref,
        thisattrDesc=attrDesc,
        thisattrComment=attrComment,
        thisattrMilieu=attrMilieu,
        thisattrChoro=attrChoro,
        thisattrConnaissance=attrConnaissance,
        thisattrHab = attrHab,
        thisattrPheno = attrPheno,
        thisattrPop = attrPop,
        thisattrIdentif = attrIdentification
    )

    descTaxon = {
        'description': None,
        'commentaire': None,
        'milieu': None,
        'chorologie': None,
        'connaissance':None,
        'habitat':None,
        'phenologie':None,
        'populations':None,
        'identification':None
    }
    for r in req:
        if r.id_attribut == attrDesc:
            descTaxon['description'] = r.valeur_attribut
        elif r.id_attribut == attrComment:
            descTaxon['commentaire'] = r.valeur_attribut
        elif r.id_attribut == attrMilieu:
            descTaxon['milieu'] = r.valeur_attribut.replace("&" , " | ")
        elif r.id_attribut == attrChoro:
            descTaxon['chorologie'] = r.valeur_attribut
        elif r.id_attribut == attrConnaissance:
            descTaxon['connaissance'] = r.valeur_attribut
        elif r.id_attribut == attrHab:
            descTaxon['habitat'] = r.valeur_attribut
        elif r.id_attribut == attrPheno:
            descTaxon['phenologie'] = r.valeur_attribut
        elif r.id_attribut == attrPop:
            descTaxon['populations'] = r.valeur_attribut
        elif r.id_attribut == attrIdentification:
            descTaxon['identification'] = r.valeur_attribut   
    return descTaxon
