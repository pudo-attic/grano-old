import unittest
from grano.core import db
from grano.test import helpers as h

from grano.test.model.test_schema import TEST_ENTITY_SCHEMA
from grano.validation.schema import validate_schema

class TestSchemaValidation(unittest.TestCase):

    def setUp(self):
        self.client = h.make_test_app()

    def tearDown(self):
        h.tear_down_test_app()

    def test_validate_basic(self):
        schema = validate_schema(TEST_ENTITY_SCHEMA)
        assert 'name' in schema
        assert 'label' in schema
        assert len(schema['attributes'])==len(TEST_ENTITY_SCHEMA['attributes'])
