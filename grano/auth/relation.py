
import grano.auth.network as network_auth
# TODO: Make sense.


def list(network):
    return network_auth.read(network)


def create(network):
    return network_auth.edit(network)


def read(network, relation):
    return network_auth.read(network)


def update(network, relation):
    return network_auth.edit(network)


def delete(network, relation):
    return network_auth.edit(network)
