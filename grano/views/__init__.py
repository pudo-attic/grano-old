from grano.core import app
from grano.util import jsonify

from grano.views.network_api import api as network_api

app.register_blueprint(network_api, url_prefix='/api/1')

@app.route('/api/1')
def apiroot():
    return jsonify({'api': 'ok', 'version': 1})
