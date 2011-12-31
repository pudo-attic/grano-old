import unittest
import json
from copy import deepcopy

from grano.test.helpers import make_test_app, tear_down_test_app
from grano.test.helpers import load_registry

class SchemaAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = make_test_app()
        load_registry()

    def tearDown(self):
        tear_down_test_app()

    def test_entity_schema_index(self):
        res = self.app.get('/api/1/schemata/entity')
        body = json.loads(res.data)
        assert len(body)==1, body
        assert body[0]=='person', body
    
    def test_relation_schema_index(self):
        res = self.app.get('/api/1/schemata/relation')
        body = json.loads(res.data)
        assert len(body)==1, body
        assert body[0]=='social', body
    
    def test_nonexisting_schema_index(self):
        res = self.app.get('/api/1/schemata/foo')
        assert res.status_code==404,res.status_code
    
    def test_entity_schema_get(self):
        res = self.app.get('/api/1/schemata/entity/person')
        body = json.loads(res.data)
        assert body['name']=='person', body
    
    def test_relation_schema_get(self):
        res = self.app.get('/api/1/schemata/relation/social')
        body = json.loads(res.data)
        assert body['name']=='social', body

    def test_relation_schema_get_not_existing(self):
        res = self.app.get('/api/1/schemata/relation/foo')
        assert res.status_code==404,res.status_code

