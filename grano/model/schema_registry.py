from collections import defaultdict

class SchemaRegistry(object):

    def __init__(self):
        self._registry = defaultdict(dict)

    def add(self, type_, schema):
        self._registry[type_][schema.name] = schema

    def get(self, type_, name):
        return self._registry[type_][name]





