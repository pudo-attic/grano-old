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
    'summary': 'This is a test',
    'type': 'person',
    'network': 'net',
    'birth_day': '2011-01-01',
    'death_day': '2012-01-01',
    'birth_place': 'Utopia'
    }


class TestEntityValidation(unittest.TestCase):

    def setUp(self):
        self.client = h.make_test_app()
        self.network = Network.create({'title': 'Net', 'slug': 'net'})
        self.schema = Schema.create(self.network, Schema.ENTITY,
                                    h.TEST_ENTITY_SCHEMA)
        db.session.commit()
        self.context = ValidationContext(network=self.network)

    def tearDown(self):
        h.tear_down_test_app()

    def test_validate_basic(self):
        try:
            validate_entity(TEST_ENTITY, self.schema, self.context)
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
