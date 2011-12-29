import unittest
import json

NETWORK_FIXTURE = {'slug': 'net', 'title': 'Test Network'}

ENTITY_FIXTURE = {'title': 'Winnie Pooh', 
                  'type': 'person',
                  'network': 'net',
                  'birth_day': '2011-01-01',
                  'birth_place': 'The Tree',
                  'death_day': '2012-01-01',
                  'description': 'Entity of the year'}

from grano.test.helpers import make_test_app, tear_down_test_app

class EntityAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = make_test_app()
        self.make_fixtures()

    def tearDown(self):
        tear_down_test_app()

    def make_fixtures(self):
        self.app.post('/api/1/networks', 
                      data=NETWORK_FIXTURE)
        res = self.app.post('/api/1/networks/net/entities', 
                      data=ENTITY_FIXTURE, 
                      follow_redirects=True)
        body = json.loads(res.data)
        self.id = body['id']

    def test_index(self):
        res = self.app.get('/api/1/networks/net/entities')
        body = json.loads(res.data)
        assert len(body)==1, body

    def test_get(self):
        res = self.app.get('/api/1/networks/net/entities/%s' % self.id)
        body = json.loads(res.data)
        assert body['title']==NETWORK_FIXTURE['title'], body

    def test_get_non_existent(self):
        res = self.app.get('/api/1/networks/bonobo')
        assert res.status_code==404,res.status_code

    def test_network_create(self):
        data = {'title': 'Banana networks', 'description': 'no'}
        res = self.app.post('/api/1/networks', data=data,
                      follow_redirects=True)
        body = json.loads(res.data)
        assert body['title']==data['title'], body

    def test_network_create_invalid(self):
        data = {'description': 'no'}
        res = self.app.post('/api/1/networks', data=data,
                      follow_redirects=True)
        assert res.status_code==400,res.status_code

    def test_network_delete_nonexistent(self):
        res = self.app.delete('/api/1/networks/the-one')
        assert res.status_code==404,res.status_code

    def test_network_delete(self):
        res = self.app.delete('/api/1/networks/the-one-percent')
        assert res.status_code==410,res.status_code
        res = self.app.get('/api/1/networks/the-one-percent')
        assert res.status_code==404,res.status_code



