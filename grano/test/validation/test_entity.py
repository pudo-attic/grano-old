import unittest
from pprint import pprint
from datetime import datetime
from copy import deepcopy

from colander import Invalid

from grano.model import Schema, Network
from grano.core import db
from grano.test import helpers as h
from grano.validation.entity import validate_entity
from grano.validation.types import ValidationContext


TEST_ENTITY = {
    'title': 'Test Person',
    'type': 'person',
    'network': 'net',
    'birth_day': '2011-01-01',
    'death_day': '2012-01-01',
    'birth_place': 'Utopia'
    }

TEST_ENTITY_OTHER = {
    'title': 'Test Person 2',
    'type': 'person',
    'network': 'net',
    'birth_day': '2010-01-01',
    'death_day': '2011-01-01',
    'birth_place': 'Hell'
    }

TEST_RELATION = {
    'type': 'social',
    'network': 'net',
    'link_type': 'friend'
    }


class TestEntityValidation(unittest.TestCase):

    def setUp(self):
        self.client = h.make_test_app()
        self.network = Network.create({'title': 'Net', 'slug': 'net'})
        self.schema = Schema.create(self.network, Schema.ENTITY,
                                    h.TEST_ENTITY_SCHEMA)
        self.rschema = Schema.create(self.network, Schema.RELATION,
                                    h.TEST_RELATION_SCHEMA)
        db.session.commit()
        self.context = ValidationContext(network=self.network)

    def tearDown(self):
        h.tear_down_test_app()

    def test_validate_basic(self):
        try:
            validate_entity(TEST_ENTITY, self.schema, self.context)
        except Invalid, i:
            assert False, i.asdict()

    def test_validate_deep(self):
        data = deepcopy(TEST_ENTITY)
        other = deepcopy(TEST_ENTITY_OTHER)
        rel = deepcopy(TEST_RELATION)
        rel['target'] = other
        data['outgoing'] = [rel]
        try:
            d = validate_entity(data, self.schema, self.context)
            #pprint(d)
            #assert False
        except Invalid, i:
            assert False, i.asdict()

    @h.raises(Invalid)
    def test_no_title(self):
        in_ = deepcopy(TEST_ENTITY)
        del in_['title']
        validate_entity(in_, self.schema, self.context)

    @h.raises(Invalid)
    def test_invalid_type(self):
        in_ = deepcopy(TEST_ENTITY)
        in_['type'] = 'animal'
        validate_entity(in_, self.schema, self.context)
