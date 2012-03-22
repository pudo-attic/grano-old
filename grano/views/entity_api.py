from flask import Blueprint, request, url_for

from grano.core import db
from grano.validation import validate_entity, ValidationContext
from grano.views.network_api import _get_network
from grano.views.common import filtered_query
from grano.util import request_content, jsonify, crossdomain
from grano.exc import Gone, NotFound, BadRequest
from grano.auth import require

api = Blueprint('entity_api', __name__)


def _get_schema(network, type_):
    schema = network.get_entity_schema(type_)
    if schema is None:
        raise BadRequest('No schema for type: %s' % type_)
    return schema


def _get_entity(slug, id):
    network = _get_network(slug)
    entity = network.Entity.current_by_id(id)
    if entity is None:
        raise NotFound('No such entity: %s' % id)
    require.entity.read(network, entity)
    return network, entity


@api.route('/<slug>/entities', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def index(slug):
    """ List all available entities. """
    network = _get_network(slug)
    require.entity.list(network)
    type_name = request.args.get('type', None)
    type_ = _get_schema(network, type_name).cls if type_name else network.Entity
    query = filtered_query(type_, request)
    return jsonify({'results': query})


@api.route('/<slug>/entities', methods=['POST'])
def create(slug):
    """ Create a new entity. """
    network = _get_network(slug)
    require.entity.create(network)
    data = request_content(request)
    context = ValidationContext(network=network)
    schema = _get_schema(network, data.get('type'))
    data = validate_entity(dict(data.items()),
            schema, context)
    entity = network.Entity.create(schema, data)
    db.session.commit()
    url = url_for('.get', slug=network.slug, id=entity.id)
    return jsonify(entity, status=201, headers={'location': url})


@api.route('/<slug>/entities/<id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get(slug, id):
    """ Get a JSON representation of the entity. """
    network, entity = _get_entity(slug, id)
    return jsonify(entity)


@api.route('/<slug>/entities/<id>/deep', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def deep(slug, id):
    """ Get a recursive JSON representation of the entity. """
    network, entity = _get_entity(slug, id)
    return jsonify(entity.as_deep_dict())


@api.route('/<slug>/entities/<id>/history', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def history(slug, id):
    """ Get a JSON representation of the entity's revision history. """
    network, entity = _get_entity(slug, id)
    return jsonify(entity.history)


@api.route('/<slug>/entities/<id>', methods=['PUT'])
def update(slug, id):
    """ Update the data of the entity. """
    network, entity = _get_entity(slug, id)
    require.entity.update(network, entity)
    data = dict(request_content(request).items())
    data['type'] = entity.type
    context = ValidationContext(network=network)
    schema = _get_schema(network, data.get('type'))
    data = validate_entity(data, schema, context)
    updated_entity = entity.update(schema, data)
    db.session.commit()
    return jsonify(updated_entity, status=202)


@api.route('/<slug>/entities/<id>', methods=['DELETE'])
def delete(slug, id):
    """ Delete the entity (or at least flag it invisible). """
    network, entity = _get_entity(slug, id)
    require.entity.delete(network, entity)
    schema = _get_schema(network, entity.type)
    entity.delete(schema)
    db.session.commit()
    raise Gone('Successfully deleted: %s' % id)
