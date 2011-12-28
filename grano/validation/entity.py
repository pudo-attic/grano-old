from grano.validation.util import mapping, key, chained, _node
from grano.validation.util import nonempty_string, in_
from grano.validation.types import NetworkSchemaType
from grano.validation.schema import apply_schema

def validate_entity(data, schema, context):
    entity = mapping('entity')
    entity.add(key('title', validator=chained(
            nonempty_string
        )))
    entity.add(key('type', validator=chained(
            nonempty_string,
            in_([schema.name])
        )))
    entity.add(key('summary', missing=None))
    entity.add(key('description', missing=None))
    entity.add(_node(NetworkSchemaType(context), 'network'))
    entity = apply_schema(entity, schema)
    return entity.deserialize(data)


