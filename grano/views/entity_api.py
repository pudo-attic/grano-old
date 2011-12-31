from flask import Blueprint, request, redirect, url_for

from grano.core import db, schema_registry
from grano.model import Entity
from grano.validation import validate_entity, ValidationContext
from grano.views.network_api import _get_network
from grano.util import request_content, jsonify
from grano.exc import Gone, NotFound, BadRequest

api = Blueprint('entity_api', __name__)

def _get_schema(type_):
    try:
        return schema_registry.get(Entity, type_)
    except KeyError:
        raise BadRequest('No schema for type: %s' % type_)

def _get_entity(id):
    entity = Entity.current_by_id(id)
    if entity is None:
        raise NotFound('No such entity: %s' % id)
    return entity

@api.route('/entities', methods=['GET'])
def index():
    """ List all available entities in the given network. """
    slugs = [e.id for e in Entity.all()]
    return jsonify(slugs)

@api.route('/networks/<slug>/entities', methods=['GET'])
def network_index(slug):
    """ List all available entities in the given network. """
    network = _get_network(slug)
    slugs = [e.id for e in Entity.all(network=network)]
    return jsonify(slugs)

@api.route('/entities', methods=['POST'])
def create():
    """ Create a new entity. """
    data = request_content(request)
    context = ValidationContext()
    schema = _get_schema(data.get('type'))
    data = validate_entity(dict(data.items()), 
            schema, context)
    entity = Entity.create(schema, data)
    db.session.commit()
    return redirect(url_for('.get', slug=entity.network.slug, 
                            id=entity.id))

@api.route('/entities/<id>', methods=['GET'])
def get(id):
    """ Get a JSON representation of the entity. """
    entity = _get_entity(id)
    return jsonify(entity)

@api.route('/entities/<id>', methods=['PUT'])
def update(id):
    """ Update the data of the entity. """
    entity = _get_entity(id)
    data = request_content(request)
    context = ValidationContext(network=entity.network)
    schema = _get_schema(data.get('type'))
    data = validate_entity(dict(data.items()), 
            schema, context)
    updated_entity = entity.update(data)
    db.session.commit()
    return jsonify(updated_entity)

@api.route('/entities/<id>', methods=['DELETE'])
def delete(id):
    """ Delete the entity (or at least flag it invisible). """
    entity = _get_entity(id)
    schema = _get_schema(entity.type)
    entity.delete(schema)
    db.session.commit()
    raise Gone('Successfully deleted: %s' % id)


