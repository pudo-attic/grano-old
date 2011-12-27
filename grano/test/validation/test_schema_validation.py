import unittest
from pprint import pprint
from copy import deepcopy

from colander import Invalid, DateTime

from grano.model import Entity, Schema
from grano.test import helpers as h

from grano.test.model.test_schema import TEST_ENTITY_SCHEMA
from grano.validation.schema import validate_schema, apply_schema
from grano.validation.util import mapping

class TestSchemaValidation(unittest.TestCase):

    def setUp(self):
        self.client = h.make_test_app()

    def tearDown(self):
        h.tear_down_test_app()

    def test_validate_basic(self):
        try:
            schema = validate_schema(TEST_ENTITY_SCHEMA)
            assert 'name' in schema
            assert 'label' in schema
            assert len(schema['attributes'])==len(TEST_ENTITY_SCHEMA['attributes'])
        except Invalid, i:
            assert False, i.asdict()

    @h.raises(Invalid)
    def test_missing_name(self):
        in_ = deepcopy(TEST_ENTITY_SCHEMA)
        del in_['name']
        validate_schema(in_)
    
    @h.raises(Invalid)
    def test_invalid_name(self):
        in_ = deepcopy(TEST_ENTITY_SCHEMA)
        in_['name'] = 'ali baba'
        validate_schema(in_)

    @h.raises(Invalid)
    def test_missing_label(self):
        in_ = deepcopy(TEST_ENTITY_SCHEMA)
        del in_['label']
        validate_schema(in_)
    
    @h.raises(Invalid)
    def test_empty_label(self):
        in_ = deepcopy(TEST_ENTITY_SCHEMA)
        in_['label'] = ''
        validate_schema(in_)
    
    @h.raises(Invalid)
    def test_attribute_missing_label(self):
        in_ = deepcopy(TEST_ENTITY_SCHEMA)
        del in_['attributes']['birth_day']['label']
        validate_schema(in_)
    
    @h.raises(Invalid)
    def test_attribute_missing_type(self):
        in_ = deepcopy(TEST_ENTITY_SCHEMA)
        del in_['attributes']['birth_day']['type']
        validate_schema(in_)
    
    @h.raises(Invalid)
    def test_attribute_invalid_type(self):
        in_ = deepcopy(TEST_ENTITY_SCHEMA)
        in_['attributes']['birth_day']['type'] = 'foo'
        validate_schema(in_)

    def test_apply_schema(self):
        base = mapping('entity')
        schema = Schema(Entity, TEST_ENTITY_SCHEMA)
        base = apply_schema(base, schema)
        assert len(base.children)==len(TEST_ENTITY_SCHEMA['attributes'])
        dd = base.children[0]
        assert dd.typ==DateTime
        assert dd.name=='death_day'
