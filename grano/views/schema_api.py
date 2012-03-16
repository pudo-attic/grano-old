from flask import Blueprint, request, redirect, url_for

from grano.core import db
from grano.util import request_content, jsonify
from grano.model import Schema
from grano.views.network_api import _get_network
from grano.validation.schema import validate_schema
from grano.exc import Gone, NotFound, BadRequest
from grano.auth import require

api = Blueprint('schema_api', __name__)


def _valid_schema(type):
    if not type in Schema.TYPES:
        raise BadRequest('Invalid schema type: %s' % type)


def _get_schema(network, type, name):
    _valid_schema(type)
    schema = {
        Schema.ENTITY: network.get_entity_schema,
        Schema.RELATION: network.get_relation_schema
        }.get(type)(name)
    if schema is None:
        raise NotFound('No schema named: %s' % name)
    require.schema.read(network, schema)
    return schema


@api.route('/<slug>/schemata/<type>', methods=['GET'])
def index(slug, type):
    """ List all available schemata for a type. """
    network = _get_network(slug)
    require.schema.list(network)
    _valid_schema(type)
    schemata = {
        Schema.ENTITY: network.entity_schemata,
        Schema.RELATION: network.relation_schemata
        }.get(type)
    return jsonify(schemata)


@api.route('/<slug>/schemata/<type>', methods=['POST'])
def create(slug, type):
    """ Create a new schema. """
    network = _get_network(slug)
    require.schema.create(network)
    _valid_schema(type)
    data = request_content(request)
    data = validate_schema(dict(data.items()))
    schema = Schema.create(network, type, data)
    db.session.commit()
    url = url_for('.get', slug=network.slug,
            type=schema.entity, name=schema.name)
    return jsonify(schema, status=201, headers={'location': url})


@api.route('/<slug>/schemata/<type>/<name>', methods=['GET'])
def get(slug, type, name):
    network = _get_network(slug)
    schema = _get_schema(network, type, name)
    return jsonify(schema)


@api.route('/<slug>/schemata/<type>/<name>', methods=['PUT'])
def update(slug, type, name):
    network = _get_network(slug)
    schema = _get_schema(network, type, name)
    require.schema.update(network, schema)
    data = request_content(request)
    data = validate_schema(dict(data.items()))
    schema.update(network, type, data)
    db.session.commit()
    return jsonify(schema, status=202)


@api.route('/<slug>/schemata/<type>/<name>', methods=['DELETE'])
def delete(slug, type, name):
    network = _get_network(slug)
    schema = _get_schema(network, type, name)
    require.schema.delete(network, schema)
    schema.delete()
    db.session.commit()
    raise Gone('Successfully deleted: %s' % name)
