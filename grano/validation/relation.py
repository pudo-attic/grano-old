from grano.validation.util import mapping

from grano.validation.schema import apply_schema

def validate_relation(data, schema):
    relation = mapping('relation')
    # TODO: valid network
    # TODO: target, source, target != source
    entity = apply_schema(relation, schema)
    return entity.deserialize(data)

