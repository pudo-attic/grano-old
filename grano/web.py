from flask import Response, request
from colander import Invalid

from grano.core import app
from grano.util import response_format, jsonify
from grano.views import *

@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
def handle_exceptions(exc):
    """ Re-format exceptions to JSON if accept requires that. """
    format = response_format(app, request)
    if format == 'json':
        body = {'status': exc.code,
                'name': exc.name,
                'description': exc.get_description(request.environ)}
        return jsonify(body, status=exc.code,
                       headers=exc.get_headers(request.environ))
    return exc

@app.errorhandler(Invalid)
def handle_validation_error(exc):
    if 'json' == response_format(app, request):
        body = {'status': 400,
                'description': unicode(exc),
                'errors': exc.as_dict()}
        return jsonify(body, status=400)
    return Response(repr(exc.unpack_errors()), status=400, 
                    mimetype='text/plain')


if __name__ == "__main__":
    app.run()


