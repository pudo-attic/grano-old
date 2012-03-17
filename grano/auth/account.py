

def list():
    return True


def create():
    from grano.core import app
    return app.config.get('REGISTRATION')


def read(account):
    return True


def update(account):
    from flaskext.login import current_user
    return current_user == account


def delete(account):
    from flaskext.login import current_user
    return current_user == account
