from grano.model import Query
from grano.validation.util import mapping, key, chained
from grano.validation.util import nonempty_string, slug_name


def available_slug(context):
    """ Check that the name is either unused or used by the quuery
    we're currently editing. """
    def _check(value):
        if context.query and context.query.name == value:
            return True
        if Query.by_name(context.network, value) is not None:
            return "This network name is already in use, please choose another."
        return True
    return _check


def query_schema(context):
    query = mapping('query')
    query.add(key('name', validator=chained(
            nonempty_string,
            available_slug(context),
            slug_name
        )))
    query.add(key('label', validator=chained(
            nonempty_string
        )))
    query.add(key('query', validator=chained(
            nonempty_string
        )))
    return query


def validate_query(data, context):
    schema = query_schema(context)
    return schema.deserialize(data)
