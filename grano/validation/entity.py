from colander import Invalid

from grano.validation.util import mapping, key, chained, sequence
from grano.validation.util import nonempty_string, in_
from grano.validation.schema import apply_schema
from grano.validation.relation import validate_relation


def entity_schema(schema):
    entity = mapping('entity')
    entity.add(key('title', validator=chained(
            nonempty_string
        )))
    entity.add(key('type', validator=chained(
            nonempty_string,
            in_([schema.name])
        )))
    return apply_schema(entity, schema)


def validate_deep(data, context, direction, attribute):
    relations = []
    node = sequence(direction)
    inv = Invalid(node)
    for i, relation_data in enumerate(data.get(direction, [])):
        try:
            other = relation_data.get(attribute, {})
            schema = context.network.get_relation_schema(relation_data.get('type'))
            if schema is None:
                raise Invalid(node, "Invalid relation type: %e" % relation_data.get('type'))
            relation = validate_relation(relation_data, schema, context, ignore_entities=True)

            schema = context.network.get_entity_schema(other.get('type'))
            if schema is None:
                raise Invalid(node, "Invalid entity type: %e" % other.get('type'))
            relation[attribute] = validate_entity(other, schema, context, deep=False)

            relations.append(relation)
        except Invalid as sub:
            inv.add(sub, i)
    return relations, inv


def validate_entity(data, schema, context, deep=True):
    schema = entity_schema(schema)
    inv = Invalid(schema)
    try:
        data = schema.deserialize(data)
    except Invalid as inv_real:
        inv = inv_real

    if deep:
        for direction, attribute in (('incoming', 'source'), ('outgoing', 'target')):
            data[direction], i = validate_deep(data, context, direction, attribute)
            if len(i.children):
                inv.add(i)

    if len(inv.children):
        raise inv
    return data
