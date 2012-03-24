from itertools import count

from flask import Blueprint, request, url_for

from grano.core import db
from grano.model import Query
from grano.validation import validate_query, ValidationContext
from grano.views.network_api import _get_network
from grano.util import request_content, jsonify, crossdomain
from grano.exc import Gone, NotFound
from grano.auth import require

api = Blueprint('query_api', __name__)


def _get_query(slug, name):
    network = _get_network(slug)
    query = Query.by_name(network, name)
    if query is None:
        raise NotFound('No such entity: %s' % name)
    require.query.read(network, query)
    return network, query


@api.route('/<slug>/queries', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def index(slug):
    """ List all available queries. """
    network = _get_network(slug)
    require.query.list(network)
    return jsonify({'results': Query.all(network)})


@api.route('/<slug>/queries', methods=['POST'])
def create(slug):
    """ Create a new query. """
    network = _get_network(slug)
    require.query.create(network)
    data = request_content(request)
    context = ValidationContext(network=network)
    data = validate_query(dict(data.items()), context)
    query = Query.create(network, data)
    db.session.commit()
    url = url_for('.get', slug=network.slug, name=query.name)
    return jsonify(query, status=201, headers={'location': url})


@api.route('/<slug>/queries/<name>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get(slug, name):
    """ Get a JSON representation of the query. """
    network, query = _get_query(slug, name)
    return jsonify(query)


@api.route('/<slug>/queries/<name>/run', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def run(slug, name):
    """ Get a JSON representation of stored queries. """
    # TODO: Use read-only DB connection
    network, query = _get_query(slug, name)
    try:
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        rp = query.run(**dict(request.args.items()))
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


@api.route('/<slug>/queries/<name>', methods=['PUT'])
def update(slug, name):
    """ Update the data of the entity. """
    network, query = _get_query(slug, name)
    require.query.update(network, query)
    context = ValidationContext(network=network, query=query)
    data = dict(request_content(request).items())
    data = validate_query(dict(data.items()), context)
    query.update(data)
    db.session.commit()
    return jsonify(query, status=202)


@api.route('/<slug>/queries/<name>', methods=['DELETE'])
def delete(slug, name):
    """ Delete the query. """
    network, query = _get_query(slug, name)
    require.query.delete(network, query)
    query.delete()
    db.session.commit()
    raise Gone('Successfully deleted: %s' % name)
