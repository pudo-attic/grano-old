from grano.validation.util import mapping, key, chained, _node
from grano.validation.util import nonempty_string, in_
from grano.validation.types import NetworkSchemaType
from grano.validation.schema import apply_schema

def validate_relation(data, schema, context):
    relation = mapping('relation')
    relation.add(key('type', validator=chained(
            nonempty_string,
            in_([schema.name])
        )))
    relation.add(_node(NetworkSchemaType(context), 'network'))
    # TODO: target, source, target != source
    entity = apply_schema(relation, schema)
    return entity.deserialize(data)

