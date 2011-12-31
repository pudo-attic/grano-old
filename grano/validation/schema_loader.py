import json
import logging

from colander import Invalid


log = logging.getLogger(__name__)

class SchemaLoader(object):

    @classmethod
    def load_file(cls, registry, file_name):
        fh = open(file_name, 'rb')
        data = json.load(fh)
        fh.close()
        return cls.load_data(registry, data)

    @classmethod
    def load_data(cls, registry, data):
        from grano.model.entity import Entity
        from grano.model.relation import Relation

        for schema_data in data.get('entity', []):
            cls.load_schema(registry, Entity, schema_data)
        for schema_data in data.get('relation', []):
            cls.load_schema(registry, Relation, schema_data)

    @classmethod
    def load_schema(cls, registry, type_, schema_data):
        from grano.model.schema import Schema
        from grano.validation.schema import validate_schema

        try:
            schema_data = validate_schema(schema_data)
            schema = Schema(type_, schema_data)
            registry.add(type_, schema)
        except Invalid, inv:
            for key, err in inv.asdict().items():
                log.error("In %s: %s", key, err)
            raise # erm...



