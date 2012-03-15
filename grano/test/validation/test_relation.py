import unittest
from pprint import pprint
from datetime import datetime
from copy import deepcopy

from colander import Invalid

from grano.model import Schema, Network
from grano.core import db
from grano.test import helpers as h
from grano.validation.relation import validate_relation
from grano.validation.entity import validate_entity
from grano.validation.types import ValidationContext

TEST_RELATION = {
    'type': 'social',
    'network': 'net',
    'link_type': 'friend'
    }

from grano.test.validation.test_entity import TEST_ENTITY

class TestRelationValidation(unittest.TestCase):

    def setUp(self):
        self.client = h.make_test_app()
        self.network = Network.create({'title': 'Net', 'slug': 'net'})
        self.schema = Schema.create(self.network, Schema.RELATION,
                                    h.TEST_RELATION_SCHEMA)
        db.session.commit()
        self.eschema = Schema.create(self.network, Schema.ENTITY,
                                     h.TEST_ENTITY_SCHEMA)
        self.context = ValidationContext(network=self.network)
        entity = deepcopy(TEST_ENTITY)
        entity['network'] = self.network.slug
        entity = validate_entity(entity, self.eschema, self.context)
        entity['title'] = 'Alice'
        a = self.network.Entity.create(self.eschema, entity)
        entity['title'] = 'Bob'
        b = self.network.Entity.create(self.eschema, entity)
        TEST_RELATION['source'] = a.id
        TEST_RELATION['target'] = b.id
        db.session.commit()

    def tearDown(self):
        h.tear_down_test_app()

    def test_validate_basic(self):
        try:
            validate_relation(TEST_RELATION, self.schema, self.context)
        except Invalid, i:
            assert False, i.asdict()

    @h.raises(Invalid)
    def test_invalid_type(self):
        in_ = deepcopy(TEST_RELATION)
        in_['type'] = 'ownedBy'
        validate_relation(in_, self.schema, self.context)

    @h.raises(Invalid)
    def test_no_source(self):
        in_ = deepcopy(TEST_RELATION)
        del in_['source']
        validate_relation(in_, self.schema, self.context)
    
    @h.raises(Invalid)
    def test_invalid_source(self):
        in_ = deepcopy(TEST_RELATION)
        in_['source'] = 'foo'
        validate_relation(in_, self.schema, self.context)

    @h.raises(Invalid)
    def test_no_target(self):
        in_ = deepcopy(TEST_RELATION)
        del in_['target']
        validate_relation(in_, self.schema, self.context)
    
    @h.raises(Invalid)
    def test_invalid_target(self):
        in_ = deepcopy(TEST_RELATION)
        in_['target'] = 'foo'
        validate_relation(in_, self.schema, self.context)
    
    @h.raises(Invalid)
    def test_source_equals_target(self):
        in_ = deepcopy(TEST_RELATION)
        in_['target'] = in_['source']
        validate_relation(in_, self.schema, self.context)
