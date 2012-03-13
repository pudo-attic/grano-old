import unittest
from grano.test import helpers as h
from grano.model.network import Network
from grano.model.schema import Schema

class TestNetwork(unittest.TestCase):

    def setUp(self):
        self.client = h.make_test_app()
        self.network = Network.create({'title': 'Net', 'slug': 'net'})
        self.eschema = Schema.create(self.network, Schema.ENTITY,
                                h.TEST_ENTITY_SCHEMA)
        self.nschema = Schema.create(self.network, Schema.RELATION,
                                h.TEST_RELATION_SCHEMA)
        self.entity = self.network.Entity.create(self.eschema, {'title': 'The Man'})

    def tearDown(self):
        h.tear_down_test_app()

    def test_raw_query(self):
        rp = self.network.raw_query("SELECT * FROM entity_person")
        rows = rp.fetchall()
        row = dict(zip(rp.keys(), rows[0]))
        assert row['title'] == self.entity.title, row

