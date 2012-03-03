
import grano.auth.network as network_auth
# TODO: Make sense.


def list(network):
    return network_auth.read(network)


def create(network):
    return network_auth.edit(network)


def read(network, entity):
    return network_auth.read(network)


def update(network, entity):
    return network_auth.edit(network)


def delete(network, entity):
    return network_auth.edit(network)
