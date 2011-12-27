import colander

from grano.validation.util import mapping, key, chained, _node
from grano.validation.util import name_wrap, nonempty_string, in_
from grano.validation.util import reserved_name, database_name

from grano.model.schema import ATTRIBUTE_TYPES_DB

INVALID_NAMES = ['id', 'current', 'serial', 'title', 
    'slug', 'type', 'incoming', 'outgoing', 'target', 'source', 
    'target_id', 'source_id', 'network', 'network_id', 
    'created_at']

ATTRIBUTE_VALIDATORS = {
    'string': colander.String,
    'float': colander.Float,
    'integer': colander.Integer,
    'date': colander.DateTime
    }

def attribute_schema(name):
    """ Validate the representation of a schema attribute. """
    schema = mapping(name, validator=chained(
        name_wrap(nonempty_string, name),
        name_wrap(reserved_name(INVALID_NAMES), name),
        name_wrap(database_name, name)
        ))
    schema.add(key('label', validator=nonempty_string))
    schema.add(key('type', validator=chained(
            nonempty_string,
            in_(ATTRIBUTE_TYPES_DB)
        )))
    return schema

def validate_schema(data):
    """ Validate a schema. This does not actually apply the 
    schema to user data but checks for the integrity of its 
    specification. """
    schema = mapping('schema')
    schema.add(key('name', validator=chained(
            nonempty_string,
            reserved_name(INVALID_NAMES),
            database_name,
        )))
    schema.add(key('label', validator=chained(
            nonempty_string,
        )))
    attributes = mapping('attributes')
    for attribute in data.get('attributes', {}):
        attributes.add(attribute_schema(attribute))
    schema.add(attributes)
    return schema.deserialize(data)


def apply_schema(base, schema):
    """ Apply the required attributes of a given schema to an existing
    schema. """
    for attribute in schema.attributes:
        validator = ATTRIBUTE_VALIDATORS[attribute.type]
        # TODO: does this need to support `missing` and `empty`.
        base.add(_node(validator, attribute.name))
    return base

