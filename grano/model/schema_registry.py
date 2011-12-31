from collections import defaultdict

class SchemaRegistry(object):

    def __init__(self):
        self._registry = defaultdict(dict)

    def add(self, type_, schema):
        self._registry[type_][schema.name] = schema

    def get(self, type_, name):
        return self._registry[type_][name]

    def list(self, type_):
        return self._registry[type_].keys()

    @property
    def types(self):
        return dict([(t.__name__.lower(), t) \
            for t in self._registry.keys()])


