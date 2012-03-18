from itertools import count

from flask import Blueprint, request, url_for

from grano.core import db, app
from grano.model import Network
from grano.validation import validate_network, ValidationContext
from grano.util import request_content, jsonify, crossdomain
from grano.exc import Gone, NotFound
from grano.auth import require

api = Blueprint('network_api', __name__)


def _get_network(slug):
    network = Network.by_slug(slug)
    if network is None:
        raise NotFound("No such network: %s" % slug)
    require.network.read(network)
    return network


@api.route('/networks', methods=['GET'])
@crossdomain(origin='*')
def index():
    """ List all available networks. """
    require.network.list()
    networks = Network.all()
    return jsonify(networks)


@api.route('/networks', methods=['POST'])
def create():
    """ Create a new network. """
    require.network.create()
    data = request_content(request)
    context = ValidationContext()
    data = validate_network(dict(data.items()), \
            context)
    network = Network.create(data)
    db.session.commit()
    url = url_for('.get', slug=network.slug)
    return jsonify(network, status=201, headers={'location': url})


@api.route('/<slug>', methods=['GET', 'OPTIONS'])
@api.route('/networks/<slug>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get(slug):
    """ Get a JSON representation of the network. """
    network = _get_network(slug)
    return jsonify(network)


@api.route('/<slug>', methods=['PUT'])
@api.route('/networks/<slug>', methods=['PUT'])
def update(slug):
    """ Update the data of the network. """
    network = _get_network(slug)
    require.network.update(network)
    data = request_content(request)
    context = ValidationContext(network=network)
    data = validate_network(dict(data.items()), \
            context)
    network.update(data)
    db.session.commit()
    return jsonify(network)


@api.route('/<slug>', methods=['DELETE'])
@api.route('/networks/<slug>', methods=['DELETE'])
def delete(slug):
    """ Delete the resource. """
    network = _get_network(slug)
    require.network.delete(network)
    network.delete()
    db.session.commit()
    raise Gone('Successfully deleted: %s' % slug)


@api.route('/<slug>/queries', methods=['GET', 'OPTIONS'])
@api.route('/networks/<slug>/queries', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def queries(slug):
    """ Get a JSON representation of stored queries. """
    #network = _get_network(slug)
    # TODO: Keep queries in DB
    return jsonify(app.config.get('STORED_QUERIES', {}))


@api.route('/<slug>/queries/<name>', methods=['GET', 'OPTIONS'])
@api.route('/networks/<slug>/queries/<name>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def query(slug, name):
    """ Get a JSON representation of stored queries. """
    # TODO: Keep queries in DB
    # TODO: Use read-only DB connection
    network = _get_network(slug)
    query = app.config.get('STORED_QUERIES', {}).get(name)
    if query is None:
        raise NotFound("No such query!")
    try:
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        rp = network.raw_query(query['query'], **dict(request.args.items()))
    except Exception as exc:
        return jsonify({'error': unicode(exc), 'query': query}, status=400)
    result = []
    for i in count():
        row = rp.fetchone()
        if row is None or i >= limit + offset:
            break
        if i < offset:
            continue
        row = dict(zip(rp.keys(), row))
        result.append(row)
    return jsonify({
            'results': result,
            'count': rp.rowcount,
            'query': query})
