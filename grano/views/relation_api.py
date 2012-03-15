from flask import Blueprint, request, redirect, url_for

from grano.core import db
from grano.validation import validate_relation, ValidationContext
from grano.views.network_api import _get_network
from grano.util import request_content, jsonify
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


@api.route('/<slug>/relations', methods=['GET'])
def index(slug):
    network = _get_network(slug)
    require.relation.list(network)
    """ List all available relations. """
    return jsonify(network.Relation.all())


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
    return redirect(url_for('.get', slug=network.slug, \
                            id=relation.id))


@api.route('/<slug>/relations/<id>', methods=['GET'])
def get(slug, id):
    """ Get a JSON representation of the relation. """
    network, relation = _get_relation(slug, id)
    return jsonify(relation)


@api.route('/<slug>/relations/<id>/history', methods=['GET'])
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
