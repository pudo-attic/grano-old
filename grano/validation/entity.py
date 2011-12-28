import colander

from grano.validation.util import mapping, key, chained
from grano.validation.util import nonempty_string, in_

from grano.validation.schema import apply_schema

def validate_entity(data, schema):
    entity = mapping('entity')
    entity.add(key('title', validator=chained(
            nonempty_string
        )))
    entity.add(key('type', validator=chained(
            nonempty_string,
            in_([schema.name])
        )))
    # TODO: valid network
    # TODO: summary
    # TODO: description
    entity = apply_schema(entity, schema)
    return entity.deserialize(data)


