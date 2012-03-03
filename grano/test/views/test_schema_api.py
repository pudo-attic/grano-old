import unittest
import json
from copy import deepcopy

from grano.core import db
from grano.model import Network, Schema
from grano.test import helpers as h
from grano.test.helpers import make_test_app, tear_down_test_app

NETWORK_FIXTURE = {'title': 'The One Percent',
                   'slug': 'net',
                   'description': 'A very neat resource!'}

ENTITY_FIXTURE = {'title': 'Winnie Pooh', 
                  'type': 'person',
                  'network': 'net',
                  'birth_day': '2011-01-01',
                  'birth_place': 'The Tree',
                  'death_day': '2012-01-01',
                  'eye_color': 'Pink',
                  'description': 'Entity of the year'}

class SchemaAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = make_test_app()
        self.app.post('/api/1/networks', 
                      data=NETWORK_FIXTURE)
        network = Network.by_slug(NETWORK_FIXTURE['slug'])
        Schema.create(network, Schema.RELATION,
                      h.TEST_RELATION_SCHEMA)
        Schema.create(network, Schema.ENTITY,
                      h.TEST_ENTITY_SCHEMA)
        db.session.commit()

    def tearDown(self):
        tear_down_test_app()

    def test_entity_schema_index(self):
        res = self.app.get('/api/1/net/schemata/entity')
        body = json.loads(res.data)
        assert len(body)==1, body
        assert body[0]['name']=='person', body

    def test_relation_schema_index(self):
        res = self.app.get('/api/1/net/schemata/relation')
        body = json.loads(res.data)
        assert len(body)==1, body
        assert body[0]['name']=='social', body
    
    def test_nonexisting_schema_index(self):
        res = self.app.get('/api/1/net/schemata/foo')
        assert res.status_code==400,res.status_code
    
    def test_entity_schema_get(self):
        res = self.app.get('/api/1/net/schemata/entity/person')
        body = json.loads(res.data)
        assert body['name']=='person', body

    def test_update(self):
        res = self.app.get('/api/1/net/schemata/entity/person')
        body = json.loads(res.data)
        body['label'] = "XXXX"
        res = self.app.put('/api/1/net/schemata/entity/person',
                data=json.dumps(body),
                content_type='application/json',
                follow_redirects=True)
        res = self.app.get('/api/1/net/schemata/entity/person')
        body2 = json.loads(res.data)
        assert body['label']==body2['label'], body2

    def test_update_add_attribute(self):
        res = self.app.get('/api/1/net/schemata/entity/person')
        body = json.loads(res.data)
        body['attributes']['eye_color'] = {
                'type': 'string',
                'label': 'Eye Color',
                'help': 'The person\' eye color.'
            }
        res = self.app.put('/api/1/net/schemata/entity/person',
                data=json.dumps(body),
                content_type='application/json',
                follow_redirects=True)
        res = self.app.get('/api/1/net/schemata/entity/person')
        body2 = json.loads(res.data)
        assert body['attributes']['eye_color']['type']=='string', \
                body['attributes']
        res = self.app.post('/api/1/net/entities',
                      data=ENTITY_FIXTURE,
                      follow_redirects=True)
        body = json.loads(res.data)
        assert body['eye_color']==ENTITY_FIXTURE['eye_color'], \
                body

    def test_relation_schema_get(self):
        res = self.app.get('/api/1/net/schemata/relation/social')
        body = json.loads(res.data)
        assert body['name']=='social', body

    def test_relation_schema_get_not_existing(self):
        res = self.app.get('/api/1/net/schemata/xxx/person')
        assert res.status_code==400,res.status_code
        res = self.app.get('/api/1/net/schemata/relation/person')
        assert res.status_code==404,res.status_code
        res = self.app.get('/api/1/net/schemata/relation/foo')
        assert res.status_code==404,res.status_code

    def test_schema_create(self):
        data = deepcopy(h.TEST_ENTITY_SCHEMA)
        data['name'] = 'duck'
        res = self.app.post('/api/1/net/schemata/entity',
                data=json.dumps(data),
                content_type='application/json',
                follow_redirects=True)
        body = json.loads(res.data)
        assert body['label']==data['label'], body

    def test_schema_create_invalid(self):
        data = deepcopy(h.TEST_ENTITY_SCHEMA)
        data['name'] = 'duck'
        del data['label']
        res = self.app.post('/api/1/net/schemata/entity',
                data=json.dumps(data),
                content_type='application/json',
                follow_redirects=True)
        assert res.status_code==400,res.status_code

    def test_schema_delete_nonexistent(self):
        res = self.app.delete('/api/1/net/schemata/entity/the-one')
        assert res.status_code==404,res.status_code

    def test_schema_delete(self):
        res = self.app.delete('/api/1/net/schemata/entity/person')
        assert res.status_code==410,res.status_code
        res = self.app.get('/api/1/net/schemata/entity/person')
        assert res.status_code==404,res.status_code
