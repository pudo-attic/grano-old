# TODO: Make sense.
from grano.auth.util import logged_in


def list():
    return True


def create():
    return logged_in()


def read(network):
    return True


def update(network):
    return logged_in()


def delete(network):
    return logged_in()
