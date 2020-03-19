
# -*- coding:utf-8 -*-
import json
import csv
from collections import OrderedDict
from io import StringIO
from flask import jsonify, Blueprint, request, current_app
from werkzeug.wrappers import Response
from . import utils
from .modeles.repositories import (
    vmSearchTaxonRepository, vmObservationsRepository,
    vmObservationsMaillesRepository, vmMedias, vmMaillesRichesse,vmCommunesRepository,vmTerritoriesRepository,vmTaxonsRepository
)
from .configuration import config

api = Blueprint('api', __name__)


@api.route('/searchTaxon', methods=['GET'])
def searchTaxonAPI():
    session = utils.loadSession()
    search = request.args.get('search', '')
    limit = request.args.get('limit', 50)
    results = vmSearchTaxonRepository.listeTaxonsSearch(session, search, limit)
    session.close()
    return jsonify(results)


@api.route('/searchCommune', methods=['GET'])
def searchCommuneAPI():
    connection = utils.engine.connect()
    search = request.args.get('search', '')
    limit = request.args.get('limit', 50)
    results = vmCommunesRepository.getCommunesSearch(connection, search, limit)
    return jsonify(results)

@api.route('/searchTerritory', methods=['GET'])
def searchTerritoryAPI():
    connection = utils.engine.connect()
    search = request.args.get('search', '')
    limit = request.args.get('limit', 50)
    results = vmTerritoriesRepository.getTerritoriesSearch(connection, search, limit)
    return jsonify(results)

@api.route('/syntheseObsCommune/<insee_com>',methods=['GET'])
def syntheseObsCommune(insee_com):
    render_format = request.args.get('format','csv')
    connection = utils.engine.connect()
    listTaxons = vmTaxonsRepository.getTaxonsCommunes(connection, insee_com,'GP')
    taxons = listTaxons['taxons']
    csvfile=StringIO()
    writer=None
    for r in taxons:
        nr=OrderedDict()
        nr['cd_nom'] = r['cd_ref']
        nr['nom_vern'] = r['nom_vern']
        nr['nom_scientifique'] = r['lb_nom']
        nr['classe'] = r['classe']
        nr['ordre'] = r['ordre']
        nr['famille'] = r['famille']
        nr['premiere_obs'] = r['first_obs']
        nr['derniere_obs'] = r['last_obs']
        try:
            nr['menace'] = r['code_lr'][0]
        except IndexError:
            nr['menace'] = None
        nr['nombre_obs'] = r['nb_obs']
        if r['sensible'] :
            nr['cd_nom'] = 0
            nr['nom_vern'] = nr['nom_scientifique'] = nr['famille'] = 'Espece sensible'
        if not writer:
            writer = csv.DictWriter(csvfile, fieldnames=list(nr.keys()), delimiter=';')
            writer.writeheader()
        writer.writerow(nr)
    csvstring=csvfile.getvalue()
    csvfile.close()
    return Response(csvstring,headers={"Content-Type":"application/csv", "Content-Disposition":"attachment;filename=\"{}.csv\"".format(insee_com) })

@api.route('/observationsMailleAndPoint/<int:cd_ref>', methods=['GET'])
def getObservationsMailleAndPointAPI(cd_ref):
    connection = utils.engine.connect()
    observations = {
        'point': vmObservationsRepository.searchObservationsChilds(connection, cd_ref),
        'maille': vmObservationsMaillesRepository.getObservationsMaillesChilds(connection, cd_ref)
    }
    connection.close()
    return jsonify(observations)


@api.route('/observationsMaille/<int:cd_ref>', methods=['GET'])
def getObservationsMailleAPI(cd_ref):
    connection = utils.engine.connect()
    observations = vmObservationsMaillesRepository.getObservationsMaillesChilds(connection, cd_ref)
    connection.close()
    return jsonify(observations)

@api.route('/observationsMailleLastObs/<int:cd_ref>',methods=['GET'])
def getObservationsMailleLastObsAPI(cd_ref):
    connection = utils.engine.connect()
    observations = vmObservationsMaillesRepository.getObservationsMaillesLastObsChilds(connection, cd_ref)
    connection.close()
    return Response(json.dumps(observations), mimetype='application/json')

@api.route('/observationsPoint/<int:cd_ref>', methods=['GET'])
def getObservationsPointAPI(cd_ref):
    connection = utils.engine.connect()
    observations = vmObservationsRepository.searchObservationsChilds(connection, cd_ref)
    connection.close()
    return jsonify(observations)


@api.route('/observations/<insee>/<int:cd_ref>', methods=['GET'])
def getObservationsCommuneTaxonAPI(insee, cd_ref):
    connection = utils.engine.connect()
    observations = vmObservationsRepository.getObservationTaxonCommune(connection, insee, cd_ref)
    connection.close()
    return jsonify(observations)


@api.route('/observationsMaille/<insee>/<int:cd_ref>', methods=['GET'])
def getObservationsCommuneTaxonMailleAPI(insee, cd_ref):
    connection = utils.engine.connect()
    observations = vmObservationsMaillesRepository.getObservationsTaxonCommuneMaille(connection, insee, cd_ref)
    connection.close()
    return jsonify(observations)

@api.route('/atlasReseau/<id_reseau>',methods=['GET'])
def getAtlasReseau(id_reseau):
    connection = utils.engine.connect()
    data = vmMaillesRichesse.getAtlasReseau(connection,id_reseau)
    connection.close()
    return Response(json.dumps(data),mimetype='application/json')

@api.route('/atlasReseau/mailles/<int:id_maille>/<id_reseau>',methods=['GET'])
def getEspecesMaille(id_maille,id_reseau):
    connection = utils.engine.connect()
    data = vmMaillesRichesse.getEspecesMaille(connection,id_maille,id_reseau)
    return Response(json.dumps(data),mimetype='application/json')

@api.route('/mailles/lastObs',methods=['GET'])
def getStatLastObsMailles():
    connection = utils.engine.connect()
    data = vmMaillesRichesse.getStatLastObsMailles(connection)
    return Response(json.dumps(data),mimetype='application/json')

@api.route('/photoGroup/<group>', methods=['GET'])
def getPhotosGroup(group):
    connection = utils.engine.connect()
    photos = vmMedias.getPhotosGalleryByGroup(
        connection, 
        current_app.config['ATTR_MAIN_PHOTO'], 
        current_app.config['ATTR_OTHER_PHOTO'], 
        group
    )
    connection.close()
    return jsonify(photos)


@api.route('/photosGallery', methods=['GET'])
def getPhotosGallery():
    connection = utils.engine.connect()
    photos = vmMedias.getPhotosGallery(
        connection, 
        current_app.config['ATTR_MAIN_PHOTO'], 
        current_app.config['ATTR_OTHER_PHOTO']
    )
    connection.close()
    return jsonify(photos)
