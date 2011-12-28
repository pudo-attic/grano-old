import unittest
from pprint import pprint
from datetime import datetime
from copy import deepcopy

from colander import Invalid

from grano.model import Schema, Relation, Network
from grano.core import db
from grano.test import helpers as h
from grano.validation.relation import validate_relation
from grano.validation.types import ValidationContext

TEST_RELATION = {
    'type': 'social',
    'network': 'net',
    'link_type': 'friend'
    }

class TestRelationValidation(unittest.TestCase):

    def setUp(self):
        self.client = h.make_test_app()
        self.schema = Schema(Relation, h.TEST_RELATION_SCHEMA)
        self.network = Network()
        self.network.title = 'Net'
        self.network.slug = 'net'
        db.session.add(self.network)
        db.session.commit()
        self.context = ValidationContext(network=self.network)

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
    def test_no_schema_attribute(self):
        in_ = deepcopy(TEST_RELATION)
        del in_['link_type']
        validate_relation(in_, self.schema, self.context)

    @h.raises(Invalid)
    def test_no_network(self):
        in_ = deepcopy(TEST_RELATION)
        del in_['network']
        validate_relation(in_, self.schema, self.context)

    @h.raises(Invalid)
    def test_invalid_network(self):
        in_ = deepcopy(TEST_RELATION)
        in_['network'] = 'not there'
        validate_relation(in_, self.schema, self.context)


