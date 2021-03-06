import unittest
from grano.core import db
from grano.test import helpers as h
from grano.model.schema import Schema
from grano.model.network import Network


class TestSchema(unittest.TestCase):

    def setUp(self):
        self.client = h.make_test_app()
        self.network = Network.create({'title': 'Net', 'slug': 'net'})

    def tearDown(self):
        h.tear_down_test_app()

    def test_basic_schema(self):
        schema = Schema.create(self.network, Schema.ENTITY,
                               h.TEST_ENTITY_SCHEMA.copy())
        assert schema.name==h.TEST_ENTITY_SCHEMA['name']
        assert schema.label==h.TEST_ENTITY_SCHEMA['label']
        assert schema.attributes.count()==4, list(schema.attributes)

    def test_attribute(self):
        schema = Schema.create(self.network, Schema.ENTITY,
                               h.TEST_ENTITY_SCHEMA)
        attr = schema.attributes[1]
        assert attr.name=='birth_day', attr.name

    def test_generate_type(self):
        schema = Schema.create(self.network, Schema.ENTITY,
                               h.TEST_ENTITY_SCHEMA)
        cls = schema.cls
        assert hasattr(cls, 'id')
        assert hasattr(cls, 'serial')
        assert hasattr(cls, 'birth_day')
        assert 'birth_day' in cls.__table__.c

