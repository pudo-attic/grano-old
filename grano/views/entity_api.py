from flask import Blueprint, request, redirect, url_for

from grano.core import db
from grano.model import Entity
from grano.validation import validate_entity, ValidationContext
from grano.views.network_api import _get_network
from grano.util import request_content, jsonify
from grano.exc import Gone, NotFound

api = Blueprint('entity_api', __name__)

def _get_entity(slug, id):
    network = _get_network(slug)
    entity = Entity.current_by_id(id)
    if entity is None:
        raise NotFound('No such entity: %s' % id)
    return network, entity

@api.route('/networks/<slug>/entities', methods=['GET'])
def index(slug):
    """ List all available entities in the given network. """
    network = _get_network(slug)
    slugs = [e.id for e in Entity.all(network=network)]
    return jsonify(slugs)

@api.route('/networks/<slug>/entities', methods=['POST'])
def create(slug):
    """ Create a new entity. """
    network = _get_network(slug)
    data = request_content(request)
    context = ValidationContext(network=network)
    # TODO: SchemaRegistry
    schema = None
    data = validate_entity(dict(data.items()), 
            schema, context)
    entity = Entity.create(schema, data)
    db.session.commit()
    return redirect(url_for('.get', slug=network.slug, id=entity.id))

@api.route('/networks/<slug>/entities/<id>', methods=['GET'])
def get(slug, id):
    """ Get a JSON representation of the entity. """
    network, entity = _get_entity(slug, id)
    return jsonify(entity)

@api.route('/network/<slug>/entities/<id>', methods=['PUT'])
def update(slug, id):
    """ Update the data of the entity. """
    network, entity = _get_entity(slug, id)
    data = request_content(request)
    context = ValidationContext(network=network)
    # TODO SchemaRegistry
    schema = None
    data = validate_entity(dict(data.items()), 
            schema, context)
    updated_entity = entity.update(data)
    db.session.commit()
    return jsonify(updated_entity)

@api.route('/networks/<slug>/entities/<id>', methods=['DELETE'])
def delete(slug):
    """ Delete the entity (or at least flag it invisible). """
    network, entity = _get_entity(slug, id)
    # TODO SchemaRegistry
    schema = None
    entity.delete(schema)
    db.session.commit()
    raise Gone('Successfully deleted: %s' % id)


