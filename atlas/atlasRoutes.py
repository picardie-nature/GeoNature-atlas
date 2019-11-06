# -*- coding:utf-8 -*-

from flask import render_template, redirect, abort, current_app, url_for
from .configuration import config
from .modeles.repositories import (
    vmTaxonsRepository,
    vmObservationsRepository,
    vmAltitudesRepository,
    vmMoisRepository,
    vmTaxrefRepository,
    vmCommunesRepository,
    vmObservationsMaillesRepository,
    vmMedias,
    vmCorTaxonAttribut,
    vmTaxonsMostView,
    vmReseauxNat,
)
from . import utils

from flask import Blueprint, request

main = Blueprint("main", __name__)


@main.route(
    "/espece/" + current_app.config["REMOTE_MEDIAS_PATH"] + "<image>",
    methods=["GET", "POST"],
)
def especeMedias(image):
    return redirect(
        current_app.config["REMOTE_MEDIAS_URL"]
        + current_app.config["REMOTE_MEDIAS_PATH"]
        + image
    )


@main.route(
    "/commune/" + current_app.config["REMOTE_MEDIAS_PATH"] + "<image>",
    methods=["GET", "POST"],
)
def communeMedias(image):
    return redirect(
        current_app.config["REMOTE_MEDIAS_URL"]
        + current_app.config["REMOTE_MEDIAS_PATH"]
        + image
    )


@main.route(
    "/liste/" + current_app.config["REMOTE_MEDIAS_PATH"] + "<image>",
    methods=["GET", "POST"],
)
def listeMedias(image):
    return redirect(
        current_app.config["REMOTE_MEDIAS_URL"]
        + current_app.config["REMOTE_MEDIAS_PATH"]
        + image
    )


@main.route(
    "/groupe/" + current_app.config["REMOTE_MEDIAS_PATH"] + "<image>",
    methods=["GET", "POST"],
)
def groupeMedias(image):
    return redirect(
        current_app.config["REMOTE_MEDIAS_URL"]
        + current_app.config["REMOTE_MEDIAS_PATH"]
        + image
    )


@main.route(
    "/" + current_app.config["REMOTE_MEDIAS_PATH"] + "<image>",
    methods=["GET", "POST"],
)
def indexMedias(image):
    return redirect(
        current_app.config["REMOTE_MEDIAS_URL"]
        + current_app.config["REMOTE_MEDIAS_PATH"]
        + image
    )


@main.route("/", methods=["GET", "POST"])
def index():
    session = utils.loadSession()
    connection = utils.engine.connect()
    if request.args.get('page')=='fiche' and request.args.get('id') and utils.idtier2cdref(request.args.get('id'),'clicnat1') : # provient d'une ancienne url clicnat 1
        return redirect(
                    url_for('main.ficheEspece',cd_ref=utils.idtier2cdref(request.args.get('id'),'clicnat1'))
                    ,code=301)
    #TODO rediriger les anciennes fiches communes
    
    if current_app.config["AFFICHAGE_MAILLE"]:
        observations = vmObservationsMaillesRepository.lastObservationsMailles(
            connection,
            current_app.config["NB_DAY_LAST_OBS"],
            current_app.config["ATTR_MAIN_PHOTO"],
        )
    else:
        observations = vmObservationsRepository.lastObservations(
            connection,
            current_app.config["NB_DAY_LAST_OBS"],
            current_app.config["ATTR_MAIN_PHOTO"],
        )

    mostViewTaxon = vmTaxonsMostView.mostViewTaxon(connection)
    stat = vmObservationsRepository.statIndex(connection)
    customStat = vmObservationsRepository.genericStat(
        connection, current_app.config["RANG_STAT"]
    )
    customStatMedias = vmObservationsRepository.genericStatMedias(
        connection, current_app.config["RANG_STAT"]
    )

    connection.close()
    session.close()

    return render_template(
        "templates/index.html",
        observations=observations,
        mostViewTaxon=mostViewTaxon,
        stat=stat,
        customStat=customStat,
        customStatMedias=customStatMedias,
    )


@main.route("/espece/<int:cd_ref>", methods=["GET", "POST"])
def ficheEspece(cd_ref):
    session = utils.loadSession()
    connection = utils.engine.connect()

    cd_ref = int(cd_ref)
    taxon = vmTaxrefRepository.searchEspece(connection, cd_ref)
    altitudes = vmAltitudesRepository.getAltitudesChilds(connection, cd_ref)
    months = vmMoisRepository.getMonthlyObservationsChilds(connection, cd_ref)
    synonyme = vmTaxrefRepository.getSynonymy(connection, cd_ref)
    communes = vmCommunesRepository.getCommunesObservationsChilds(connection, cd_ref)
    taxonomyHierarchy = vmTaxrefRepository.getAllTaxonomy(session, cd_ref)
    firstPhoto = vmMedias.getFirstPhoto(
        connection, cd_ref, current_app.config["ATTR_MAIN_PHOTO"]
    )
    photoCarousel = vmMedias.getPhotoCarousel(
        connection, cd_ref, current_app.config["ATTR_OTHER_PHOTO"]
    )
    videoAudio = vmMedias.getVideo_and_audio(
        connection,
        cd_ref,
        current_app.config["ATTR_AUDIO"],
        current_app.config["ATTR_VIDEO_HEBERGEE"],
        current_app.config["ATTR_YOUTUBE"],
        current_app.config["ATTR_DAILYMOTION"],
        current_app.config["ATTR_VIMEO"],
    )
    articles = vmMedias.getLinks_and_articles(
        connection,
        cd_ref,
        current_app.config["ATTR_LIEN"],
        current_app.config["ATTR_PDF"],
    )
    taxonDescription = vmCorTaxonAttribut.getAttributesTaxon(
        connection,
        cd_ref,
        current_app.config["ATTR_DESC"],
        current_app.config["ATTR_COMMENTAIRE"],
        current_app.config["ATTR_MILIEU"],
        current_app.config["ATTR_CHOROLOGIE"],
        current_app.config["ATTR_CONNAISSANCE"],
        current_app.config["ATTR_HAB"],
        current_app.config["ATTR_PHENO"],
        current_app.config["ATTR_POP"]
    )
    observers = vmObservationsRepository.getObservers(connection, cd_ref)

    connection.close()
    session.close()

    return render_template(
        "templates/ficheEspece.html",
        taxon=taxon,
        listeTaxonsSearch=[],
        observations=[],
        cd_ref=cd_ref,
        altitudes=altitudes,
        months=months,
        synonyme=synonyme,
        communes=communes,
        taxonomyHierarchy=taxonomyHierarchy,
        firstPhoto=firstPhoto,
        photoCarousel=photoCarousel,
        videoAudio=videoAudio,
        articles=articles,
        taxonDescription=taxonDescription,
        observers=observers,
    )


@main.route("/commune/<insee>", methods=["GET", "POST"])
def ficheCommune(insee):
    session = utils.loadSession()
    connection = utils.engine.connect()

    listTaxons = vmTaxonsRepository.getTaxonsCommunes(connection, insee,'GP')
    commune = vmCommunesRepository.getCommuneFromInsee(connection, insee)
    communesSearch = vmCommunesRepository.getAllCommunes(session)
    if config.AFFICHAGE_MAILLE:
        observations = vmObservationsMaillesRepository.lastObservationsCommuneMaille(
            connection, config.NB_LAST_OBS, insee
        )
    else:
        observations = vmObservationsRepository.lastObservationsCommune(
            connection, config.NB_LAST_OBS, insee
        )

    observers = vmObservationsRepository.getObserversCommunes(
        connection, insee
    )

    reseaux = vmReseauxNat.getAllReseaux(connection,public_cible='GP')
    reseaux.append({'code_reseau':'autre','nom_reseau':u'Autres espèces','id_reseau':99,'int_sort':99})
    
    data_by_reseau = list()
    for r in reseaux : #reseaux publics
        taxons = list(filter(lambda k : k['code_reseau_gp'] == r['code_reseau'], listTaxons['taxons']))
        n_sp_protected = len(list(filter(lambda k : k['protected'] == True, taxons)))
        n_sp_threatened = len(list(filter(lambda k : k['threatened'] == True, taxons)))
        n_sp_sensible = len(list(filter(lambda k : k['sensible'] == True, taxons)))
        data_by_reseau.append({
            'nom_reseau':r['nom_reseau'],
            'code_reseau':r['code_reseau'],
            'picto_reseau':r.get('picto_reseau',''),
            'n_sp_protected':n_sp_protected, 'n_sp_threatened' : n_sp_threatened, 'n_sp_sensible':n_sp_sensible,'n_sp': len(taxons),
            'int_sort':r.get('int_sort',0), #"Autre" à 99, les autres à 0
            'taxons':taxons})
    """
    configuration = base_configuration.copy()
    configuration.update({
        'NB_LAST_OBS': config.NB_LAST_OBS,
        'AFFICHAGE_MAILLE': config.AFFICHAGE_MAILLE,
        'MAP': config.MAP,
        'MYTYPE': 1,
        'PATRIMONIALITE': config.PATRIMONIALITE,
        'PROTECTION': config.PROTECTION
    })"""

    session.close()
    connection.close()

    return render_template(
        'templates/ficheCommune.html',
        listTaxons=listTaxons,
        referenciel=commune,
        communesSearch=communesSearch,
        observations=observations,
        observers=observers,
        reseaux=reseaux,
        #configuration=configuration,
        data = data_by_reseau
)


@main.route("/liste/<cd_ref>", methods=["GET", "POST"])
def ficheRangTaxonomie(cd_ref):
    session = utils.loadSession()
    connection = utils.engine.connect()

    listTaxons = vmTaxonsRepository.getTaxonsChildsList(connection, cd_ref)
    referenciel = vmTaxrefRepository.getInfoFromCd_ref(session, cd_ref)
    taxonomyHierarchy = vmTaxrefRepository.getAllTaxonomy(session, cd_ref)
    observers = vmObservationsRepository.getObservers(connection, cd_ref)

    connection.close()
    session.close()

    return render_template(
        "templates/ficheRangTaxonomique.html",
        listTaxons=listTaxons,
        referenciel=referenciel,
        taxonomyHierarchy=taxonomyHierarchy,
        observers=observers,
        DISPLAY_EYE_ON_LIST=False,
    )


@main.route("/groupe/<groupe>", methods=["GET", "POST"])
def ficheGroupe(groupe):
    session = utils.loadSession()
    connection = utils.engine.connect()

    groups = vmTaxonsRepository.getAllINPNgroup(connection)
    listTaxons = vmTaxonsRepository.getTaxonsGroup(connection, groupe)
    observers = vmObservationsRepository.getGroupeObservers(connection, groupe)

    session.close()
    connection.close()

    return render_template(
        "templates/ficheGroupe.html",
        listTaxons=listTaxons,
        referenciel=groupe,
        groups=groups,
        observers=observers,
        DISPLAY_EYE_ON_LIST=False,
    )


@main.route("/photos", methods=["GET", "POST"])
def photos():
    session = utils.loadSession()
    connection = utils.engine.connect()

    groups = vmTaxonsRepository.getINPNgroupPhotos(connection)

    session.close()
    connection.close()
    return render_template("templates/galeriePhotos.html", groups=groups)


@main.route("/<page>", methods=["GET", "POST"])
def get_staticpages(page):
    session = utils.loadSession()
    if page not in current_app.config["STATIC_PAGES"]:
        abort(404)
    static_page = current_app.config["STATIC_PAGES"][page]
    session.close()
    return render_template(static_page["template"])

