from flask import Response, request
from colander import Invalid
from hashlib import sha1

from grano.model import Account
from grano.core import app, current_user, login_manager
from grano.util import response_format, jsonify, login_user
from grano.util import validate_cache, NotModified
from grano.exc import Unauthorized
from grano import auth
from grano.views import *


@app.context_processor
def set_template_context():
    """ Set some template context globals. """
    return dict(current_user=current_user,
                can=auth)


@login_manager.user_loader
def load_account(name):
    return Account.by_name(name)


@app.after_request
def configure_caching(response_class):
    if request.method != 'GET' or response_class.status_code > 399:
        return response_class
    try:
        etag, mod_time = validate_cache(request)
    except NotModified:
        return Response(status=304)
    response_class.add_etag(etag)
    response_class.cache_control.max_age = 21600
    if current_user.is_anonymous():
        response_class.cache_control.public = True
        response_class.headers.remove('Set-Cookie')
    else:
        response_class.cache_control.private = True
    if mod_time:
        response_class.last_modified = mod_time
    return response_class


@app.before_request
def setup_cache():
    args = request.args.items()
    args = filter(lambda (k,v): k != '_', args) # haha jquery where is your god now?!?
    query = sha1(repr(sorted(args))).hexdigest()
    request.cache_key = {'query': query}


@app.before_request
def basic_authentication():
    """ Attempt HTTP basic authentication on a per-request basis. """
    if 'Authorization' in request.headers:
        authorization = request.headers.get('Authorization')
        authorization = authorization.split(' ', 1)[-1]
        name, password = authorization.decode('base64').split(':', 1)
        account = Account.by_name(name)
        if account is None \
            or not account.validate_password(password) \
            or not login_user(account):
            raise Unauthorized('Invalid username or password.')


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


@app.errorhandler(NotModified)
def handle_not_modified(exc):
    return Response(status=304)


if __name__ == "__main__":
    app.run(port=5002)
