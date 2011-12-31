from flask import Blueprint

from grano.model import schema_registry
from grano.util import jsonify
from grano.exc import NotFound

api = Blueprint('schema_api', __name__)

@api.route('/schemata/<type>', methods=['GET'])
def index(type):
    """ List all available schemata for a type. """
    if not type in schema_registry.types:
        raise NotFound("%s is not a known type!" % type)
    type_ = schema_registry.types[type]
    names = schema_registry.list(type_)
    return jsonify(names)

@api.route('/schemata/<type>/<name>', methods=['GET'])
def get(type, name):
    if not type in schema_registry.types:
        raise NotFound("%s is not a known type!" % type)
    type_ = schema_registry.types[type]
    try:
        schema = schema_registry.get(type_, name)
        return jsonify(schema)
    except KeyError:
        raise NotFound("Schema %s cannot be found!" % name)
