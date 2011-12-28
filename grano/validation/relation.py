from grano.validation.util import mapping, key, chained
from grano.validation.util import nonempty_string, in_

from grano.validation.schema import apply_schema

def validate_relation(data, schema):
    relation = mapping('relation')
    relation.add(key('type', validator=chained(
            nonempty_string,
            in_([schema.name])
        )))
    # TODO: valid network
    # TODO: target, source, target != source
    entity = apply_schema(relation, schema)
    return entity.deserialize(data)

