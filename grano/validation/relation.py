from grano.validation.util import mapping, key, chained, _node
from grano.validation.util import nonempty_string, in_
from grano.validation.types import NetworkSchemaType, EntitySchemaType
from grano.validation.schema import apply_schema

def source_not_target(data):
    if data.get('source') and data.get('source') == data.get('target'):
        return "The relation points at itself."
    return True

def validate_relation(data, schema, context):
    relation = mapping('relation', validator=chained(
            source_not_target
        ))
    relation.add(key('type', validator=chained(
            nonempty_string,
            in_([schema.name])
        )))
    relation.add(_node(NetworkSchemaType(context), 'network'))
    relation.add(_node(EntitySchemaType(context), 'source'))
    relation.add(_node(EntitySchemaType(context), 'target'))
    entity = apply_schema(relation, schema)
    return entity.deserialize(data)

