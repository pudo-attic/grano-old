from flask import Response, request
from colander import Invalid

from grano.model import Account
from grano.core import app, current_user, login_manager
from grano.util import response_format, jsonify, invalid_dict
from grano.views import *


@app.context_processor
def set_template_context():
    """ Set some template context globals. """
    return dict(current_user=current_user)


@login_manager.user_loader
def load_account(name):
    return Account.by_name(name)


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
                'errors': exc.asdict()}
        return jsonify(body, status=400)
    return Response(repr(exc.asdict()), status=400,
                    mimetype='text/plain')


if __name__ == "__main__":
    app.run()


