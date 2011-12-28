from flask import Blueprint, request, redirect, url_for

from grano.model import Network
from grano.util import request_content, jsonify
from grano.exc import Gone

api = Blueprint('network_api', __name__)

@api.route('/networks', methods=['GET'])
def index():
    """ List all available networks. """
    return jsonify(list(Network.all()))


