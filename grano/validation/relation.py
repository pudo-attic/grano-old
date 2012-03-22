from grano.validation.util import mapping, key, chained, _node
from grano.validation.util import nonempty_string, in_
from grano.validation.types import EntitySchemaType
from grano.validation.schema import apply_schema


def source_not_target(data):
    if data.get('source') and data.get('source') == data.get('target'):
        return "The relation points at itself."
    return True


def relation_schema(schema, context, ignore_entities=False):
    relation = mapping('relation', validator=chained(
            source_not_target
        ))
    relation.add(key('type', validator=chained(
            nonempty_string,
            in_([schema.name])
        )))
    if not ignore_entities:
        relation.add(_node(EntitySchemaType(context), 'source'))
        relation.add(_node(EntitySchemaType(context), 'target'))
    return apply_schema(relation, schema)


def validate_relation(data, schema, context, ignore_entities=False):
    schema = relation_schema(schema, context,
        ignore_entities=ignore_entities)
    return schema.deserialize(data)
