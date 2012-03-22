from flask import Blueprint, request, url_for

from grano.core import db
from grano.validation import validate_relation, ValidationContext
from grano.views.network_api import _get_network
from grano.views.common import filtered_query
from grano.util import request_content, jsonify, crossdomain
from grano.exc import Gone, NotFound, BadRequest
from grano.auth import require

api = Blueprint('relation_api', __name__)


def _get_schema(network, type_):
    schema = network.get_relation_schema(type_)
    if schema is None:
        raise BadRequest('No schema for type: %s' % type_)
    return schema


def _get_relation(slug, id):
    network = _get_network(slug)
    relation = network.Relation.current_by_id(id)
    if relation is None:
        raise NotFound('No such entity: %s' % id)
    require.relation.read(network, relation)
    return network, relation


@api.route('/<slug>/relations', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def index(slug):
    """ List all available relations. """
    network = _get_network(slug)
    require.relation.list(network)
    type_name = request.args.get('type', None)
    type_ = _get_schema(network, type_name).cls if type_name else network.Relation
    query = filtered_query(type_, request)
    return jsonify({'results': query})


@api.route('/<slug>/relations', methods=['POST'])
def create(slug):
    """ Create a new relation. """
    network = _get_network(slug)
    require.relation.create(network)
    data = request_content(request)
    context = ValidationContext(network=network)
    schema = _get_schema(network, data.get('type'))
    data = validate_relation(dict(data.items()), \
            schema, context)
    relation = network.Relation.create(schema, data)
    db.session.commit()
    url = url_for('.get', slug=network.slug, id=relation.id)
    return jsonify(relation, status=201, headers={'location': url})


@api.route('/<slug>/relations/<id>', methods=['GET'])
@crossdomain(origin='*')
def get(slug, id):
    """ Get a JSON representation of the relation. """
    network, relation = _get_relation(slug, id)
    return jsonify(relation)


@api.route('/<slug>/relations/<id>/deep', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def deep(slug, id):
    """ Get a recursive JSON representation of the relation. """
    network, relation = _get_relation(slug, id)
    return jsonify(relation.as_deep_dict())


@api.route('/<slug>/relations/<id>/history', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def history(slug, id):
    """ Get a JSON representation of the relation. """
    network, relation = _get_relation(slug, id)
    return jsonify(relation.history)


@api.route('/<slug>/relations/<id>', methods=['PUT'])
def update(slug, id):
    """ Update the data of the relation. """
    network, relation = _get_relation(slug, id)
    require.relation.update(network, relation)
    data = dict(request_content(request).items())
    data['type'] = relation.type
    context = ValidationContext(network=network)
    schema = _get_schema(network, data.get('type'))
    data = validate_relation(data, schema, context)
    updated_relation = relation.update(schema, data)
    db.session.commit()
    return jsonify(updated_relation)


@api.route('/<slug>/relations/<id>', methods=['DELETE'])
def delete(slug, id):
    """ Delete the relation (or at least flag it invisible). """
    network, relation = _get_relation(slug, id)
    require.relation.delete(network, relation)
    schema = _get_schema(network, relation.type)
    relation.delete(schema)
    db.session.commit()
    raise Gone('Successfully deleted: %s' % id)
