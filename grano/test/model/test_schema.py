import unittest
from grano.core import db
from grano.test import helpers
from grano.model.schema import Schema, Attribute
from grano.model.entity import Entity

TEST_SCHEMA = {
    'name': 'person2',
    'label': 'Person',
    'attributes': {
        'birth_day': {
            'type': 'date',
            'label': 'Birth Day',
            'help': 'The person\'s birth day.'
            },
        'death_day': {
            'type': 'date',
            'label': 'Death Day',
            'help': 'The day the person died.'
            },
        'birth_place': {
            'type': 'string',
            'label': 'Birth Place',
            'help': 'The place of birth.'
            }
        }
    }


class TestSchema(unittest.TestCase):

    def setUp(self):
        self.client = helpers.make_test_app()

    def tearDown(self):
        helpers.tear_down_test_app()

    def test_basic_schema(self):
        schema = Schema(Entity, TEST_SCHEMA)
        assert schema.name==TEST_SCHEMA['name']
        assert schema.label==TEST_SCHEMA['label']
        assert len(schema.attributes)==3, schema.attributes
    
    def test_attribute(self):
        schema = Schema(Entity, TEST_SCHEMA)
        attr = schema.attributes[1]
        assert attr.name=='birth_day', attr.name
        assert attr.column_type==db.DateTime

    def test_generate_type(self):
        schema = Schema(Entity, TEST_SCHEMA)
        cls = schema.cls
        assert hasattr(cls, 'id')
        assert hasattr(cls, 'serial')
        assert hasattr(cls, 'birth_day')
        assert 'birth_day' in cls.__table__.c

