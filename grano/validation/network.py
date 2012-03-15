
INVALID_NETWORK_NAMES = ['network', 'networks', 'api', 'types']

from grano.model import Network
from grano.model.util import slugify
from grano.validation.util import mapping, key, chained
from grano.validation.util import nonempty_string, slug_name


def available_slug(context):
    """ Check that the slug is either unused or used by the network
    we're currently editing. """
    def _check(value):
        if context.network and context.network.slug == value:
            return True
        if Network.by_slug(value) is not None:
            return "This network name is already in use, please choose another."
        return True
    return _check


def validate_network(data, context):
    network = mapping('network')
    network.add(key('slug', validator=chained(
            nonempty_string,
            slug_name,
            available_slug(context)
        )))
    network.add(key('title', validator=nonempty_string))
    network.add(key('description', missing=None))
    if not 'slug' in data:
        data['slug'] = slugify(data.get('title', ''))
    return network.deserialize(data)
