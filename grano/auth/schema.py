import network as network_auth


def list(network):
    return network_auth.read(network)


def create(network):
    return network_auth.update(network)


def read(network, schema):
    return network_auth.read(network)


def update(network, schema):
    return network_auth.update(network)


def delete(network, schema):
    return network_auth.update(network)
