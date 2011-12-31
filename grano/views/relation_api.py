from flask import Blueprint, request, redirect, url_for

from grano.core import db
from grano.model import Relation, schema_registry
from grano.validation import validate_relation, ValidationContext
from grano.views.network_api import _get_network
from grano.util import request_content, jsonify
from grano.exc import Gone, NotFound, BadRequest

api = Blueprint('relation_api', __name__)

def _get_schema(type_):
    try:
        return schema_registry.get(Relation, type_)
    except KeyError:
        raise BadRequest('No schema for type: %s' % type_)

def _get_relation(id):
    relation = Relation.current_by_id(id)
    if relation is None:
        raise NotFound('No such entity: %s' % id)
    return relation

@api.route('/relations', methods=['GET'])
def index():
    """ List all available relations. """
    ids = [e.id for e in Relation.all()]
    return jsonify(ids)

@api.route('/networks/<slug>/relations', methods=['GET'])
def network_index(slug):
    """ List all available relations in the given network. """
    network = _get_network(slug)
    ids = [e.id for e in Relation.all(network=network)]
    return jsonify(ids)

@api.route('/relations', methods=['POST'])
def create():
    """ Create a new relation. """
    data = request_content(request)
    context = ValidationContext()
    schema = _get_schema(data.get('type'))
    data = validate_relation(dict(data.items()), 
            schema, context)
    relation = Relation.create(schema, data)
    db.session.commit()
    return redirect(url_for('.get', slug=relation.network.slug, 
                            id=relation.id))

@api.route('/relations/<id>', methods=['GET'])
def get(id):
    """ Get a JSON representation of the relation. """
    relation = _get_relation(id)
    return jsonify(relation)

@api.route('/relations/<id>/history', methods=['GET'])
def history(id):
    """ Get a JSON representation of the relation. """
    relation = _get_relation(id)
    return jsonify(relation.history)

@api.route('/relations/<id>', methods=['PUT'])
def update(id):
    """ Update the data of the relation. """
    relation = _get_relation(id)
    data = dict(request_content(request).items())
    data['type'] = relation.type
    context = ValidationContext(network=relation.network)
    schema = _get_schema(data.get('type'))
    data = validate_relation(data, schema, context)
    updated_relation = relation.update(schema, data)
    db.session.commit()
    print "UPDATED", updated_relation
    return jsonify(updated_relation)

@api.route('/relations/<id>', methods=['DELETE'])
def delete(id):
    """ Delete the relation (or at least flag it invisible). """
    relation = _get_relation(id)
    schema = _get_schema(relation.type)
    relation.delete(schema)
    db.session.commit()
    raise Gone('Successfully deleted: %s' % id)



