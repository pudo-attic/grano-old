import unittest
import json
from copy import deepcopy


NETWORK_FIXTURE = {'slug': 'net', 'title': 'Test Network'}

ENTITY2_FIXTURE = {'title': 'Calvin', 
                  'type': 'person',
                  'network': 'net',
                  'birth_day': '2011-01-01',
                  'birth_place': 'The Tree',
                  'death_day': '2012-01-01',
                  'description': 'A school boy'}

ENTITY1_FIXTURE = {'title': 'Hobbes', 
                  'type': 'person',
                  'network': 'net',
                  'birth_day': '2011-01-01',
                  'birth_place': 'The Tree',
                  'death_day': '2012-01-01',
                  'description': 'A teddy bear'}

RELATION_FIXTURE = {'network': 'net', 'link_type': 'friendOf', 'type': 'social'}

from grano.test.helpers import make_test_app, tear_down_test_app
from grano.test.helpers import load_registry

class RelationAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = make_test_app()
        load_registry()
        self.make_fixtures()

    def tearDown(self):
        tear_down_test_app()

    def make_fixtures(self):
        self.app.post('/api/1/networks', 
                      data=NETWORK_FIXTURE)
        res = self.app.post('/api/1/entities', 
                      data=ENTITY1_FIXTURE, 
                      follow_redirects=True)
        body = json.loads(res.data)
        self.source_id = body['id']
        res = self.app.post('/api/1/entities', 
                      data=ENTITY2_FIXTURE, 
                      follow_redirects=True)
        body = json.loads(res.data)
        self.target_id = body['id']
        RELATION_FIXTURE['source'] = self.source_id
        RELATION_FIXTURE['target'] = self.target_id
        res = self.app.post('/api/1/relations', 
                      data=RELATION_FIXTURE, 
                      follow_redirects=True)
        print res.data
        body = json.loads(res.data)
        self.id = body['id']

    def test_network_index(self):
        res = self.app.get('/api/1/networks/net/relations')
        body = json.loads(res.data)
        assert len(body)==1, body
    
    def test_index(self):
        res = self.app.get('/api/1/relations')
        body = json.loads(res.data)
        assert len(body)==1, body

    def test_get(self):
        res = self.app.get('/api/1/relations/%s' % self.id)
        body = json.loads(res.data)
        assert body['link_type']==RELATION_FIXTURE['link_type'], body

    def test_get_non_existent(self):
        res = self.app.get('/api/1/relations/bonobo')
        assert res.status_code==404,res.status_code

    def test_relation_create(self):
        data = deepcopy(RELATION_FIXTURE)
        data['link_type'] = 'toyOf'
        res = self.app.post('/api/1/relations', data=data,
                      follow_redirects=True)
        body = json.loads(res.data)
        assert body['link_type']==data['link_type'], body

    def test_relation_create_invalid(self):
        data = {'source': 'no', 'target': self.target_id}
        res = self.app.post('/api/1/relations', data=data,
                      follow_redirects=True)
        assert res.status_code==400,res.status_code

    def test_relation_delete_nonexistent(self):
        res = self.app.delete('/api/1/relations/the-one')
        assert res.status_code==404,res.status_code

    def test_relation_delete(self):
        res = self.app.delete('/api/1/relations/%s' % self.id)
        assert res.status_code==410,res.status_code
        res = self.app.get('/api/1/relations/%s' % self.id)
        assert res.status_code==404,res.status_code




