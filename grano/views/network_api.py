from flask import Blueprint, request, url_for, Response

import networkx as nx

from grano.core import db
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


@api.route('/<slug>/graph', methods=['GET', 'OPTIONS'])
@api.route('/networks/<slug>/graph', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def graph(slug):
    """ Get a JSON representation of the network. """
    network = _get_network(slug)
    graph = nx.DiGraph()

    for entity in network.entities:
        entity.as_nx(graph)
    for relation in network.relations:
        relation.as_nx(graph)

    out = ''
    for line in nx.generate_gexf(graph):
        #print [line]
        out += line

    return Response(out, status=200,
        content_type='text/xml')


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
