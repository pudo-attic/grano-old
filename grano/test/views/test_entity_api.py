import unittest
import json
from copy import deepcopy

from grano.test.helpers import AUTHZ_HEADER

NETWORK_FIXTURE = {'slug': 'net', 'title': 'Test Network'}

ENTITY_FIXTURE = {'title': 'Winnie Pooh', 
                  'type': 'person',
                  'network': 'net',
                  'birth_day': '2011-01-01',
                  'birth_place': 'The Tree',
                  'death_day': '2012-01-01'}

from grano.core import db
from grano.model import Network, Schema
from grano.test import helpers as h
from grano.test.helpers import make_test_app, tear_down_test_app

class EntityAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = make_test_app()
        self.make_fixtures()

    def tearDown(self):
        tear_down_test_app()

    def make_fixtures(self):
        self.app.post('/api/1/networks',
                    headers=AUTHZ_HEADER,
                    data=NETWORK_FIXTURE)
        network = Network.by_slug(NETWORK_FIXTURE['slug'])
        Schema.create(network, Schema.RELATION,
                      h.TEST_RELATION_SCHEMA)
        Schema.create(network, Schema.ENTITY,
                      h.TEST_ENTITY_SCHEMA)
        db.session.commit()
        res = self.app.post('/api/1/net/entities', 
                    headers=AUTHZ_HEADER,
                    data=ENTITY_FIXTURE, 
                    follow_redirects=True)
        body = json.loads(res.data)
        self.id = body['id']

    def test_network_index(self):
        res = self.app.get('/api/1/net/entities')
        body = json.loads(res.data)
        assert len(body)==1, body
    
    def test_get(self):
        res = self.app.get('/api/1/net/entities/%s' % self.id)
        body = json.loads(res.data)
        assert body['title']==ENTITY_FIXTURE['title'], body
    
    def test_get(self):
        res = self.app.get('/api/1/net/entities/%s/history' % self.id)
        body = json.loads(res.data)
        assert len(body)==1,body

    def test_get_non_existent(self):
        res = self.app.get('/api/1/net/entities/bonobo')
        assert res.status_code==404,res.status_code

    def test_entity_create(self):
        data = deepcopy(ENTITY_FIXTURE)
        data['title'] = 'Tigger'
        res = self.app.post('/api/1/net/entities', data=data,
                    headers=AUTHZ_HEADER,
                    follow_redirects=True)
        body = json.loads(res.data)
        assert body['title']==data['title'], body

    def test_entity_create_invalid(self):
        data = {'description': 'no'}
        res = self.app.post('/api/1/net/entities', data=data,
                    headers=AUTHZ_HEADER,
                    follow_redirects=True)
        assert res.status_code==400,res.status_code
    
    def test_update(self):
        res = self.app.get('/api/1/net/entities/%s' % self.id)
        body = json.loads(res.data)
        t = 'A banana'
        body['title'] = t
        res = self.app.put('/api/1/net/entities/%s' % self.id, 
                    headers=AUTHZ_HEADER,
                    data=body)
        assert res.status_code==202,res.status_code
        body = json.loads(res.data)
        assert body['title']==t, body
        
        res = self.app.get('/api/1/net/entities/%s/history' % self.id)
        body = json.loads(res.data)
        assert len(body)==2,body

    def test_entity_delete_nonexistent(self):
        res = self.app.delete('/api/1/net/entities/the-one',
                    headers=AUTHZ_HEADER)
        assert res.status_code==404,res.status_code

    def test_entity_delete(self):
        res = self.app.delete('/api/1/net/entities/%s' % self.id,
                    headers=AUTHZ_HEADER)
        assert res.status_code==410,res.status_code
        res = self.app.get('/api/1/net/entities/%s' % self.id)
        assert res.status_code==404,res.status_code
