import unittest
from pprint import pprint
from datetime import datetime
from copy import deepcopy

from colander import Invalid

from grano.model import Schema, Relation
from grano.test import helpers as h
from grano.validation.relation import validate_relation

TEST_RELATION = {
    'type': 'social',
    'network': 'foo',
    'link_type': 'friend'
    }

class TestEntityValidation(unittest.TestCase):

    def setUp(self):
        self.client = h.make_test_app()
        self.schema = Schema(Relation, h.TEST_RELATION_SCHEMA)

    def tearDown(self):
        h.tear_down_test_app()

    def test_validate_basic(self):
        try:
            validate_relation(TEST_RELATION, self.schema)
        except Invalid, i:
            assert False, i.asdict()

    @h.raises(Invalid)
    def test_invalid_type(self):
        in_ = deepcopy(TEST_RELATION)
        in_['type'] = 'ownedBy'
        validate_relation(in_, self.schema)

    @h.raises(Invalid)
    def test_no_schema_attribute(self):
        in_ = deepcopy(TEST_RELATION)
        del in_['link_type']
        validate_relation(in_, self.schema)



