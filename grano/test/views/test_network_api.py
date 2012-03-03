import unittest
import json

NETWORK_FIXTURE = {'title': 'The One Percent', 
                   'description': 'A very neat resource!'}

from grano.test.helpers import make_test_app, tear_down_test_app
from grano.test.helpers import AUTHZ_HEADER

class NetworkAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = make_test_app()
        self.make_fixtures()

    def tearDown(self):
        tear_down_test_app()

    def make_fixtures(self):
        self.app.post('/api/1/networks',
                    headers=AUTHZ_HEADER,
                    data=NETWORK_FIXTURE)

    def test_network_index(self):
        res = self.app.get('/api/1/networks')
        body = json.loads(res.data)
        assert len(body)==1, body

    def test_network_get(self):
        res = self.app.get('/api/1/the-one-percent')
        body = json.loads(res.data)
        assert body['title']==NETWORK_FIXTURE['title'], body

    def test_network_get_non_existent(self):
        res = self.app.get('/api/1/bonobo')
        assert res.status_code==404,res.status_code

    def test_network_create(self):
        data = {'title': 'Banana networks', 'description': 'no'}
        res = self.app.post('/api/1/networks', data=data,
                    headers=AUTHZ_HEADER,
                    follow_redirects=True)
        body = json.loads(res.data)
        assert body['title']==data['title'], body

    def test_network_create_invalid(self):
        data = {'description': 'no'}
        res = self.app.post('/api/1/networks', data=data,
                    headers=AUTHZ_HEADER,
                    follow_redirects=True)
        assert res.status_code==400,res.status_code
    
    def test_network_update(self):
        res = self.app.get('/api/1/the-one-percent')
        body = json.loads(res.data)
        t = 'Spidernet'
        body['title'] = t
        res = self.app.put('/api/1/the-one-percent',
                        headers=AUTHZ_HEADER,
                        data=body)
        assert res.status_code==200, res.status_code
        body = json.loads(res.data)
        assert body['title']==t, body

    def test_network_delete_nonexistent(self):
        res = self.app.delete('/api/1/the-one')
        assert res.status_code==404, res.status_code

    def test_network_delete(self):
        res = self.app.delete('/api/1/the-one-percent',
                    headers=AUTHZ_HEADER)
        assert res.status_code==410, res.status_code
        res = self.app.get('/api/1/the-one-percent')
        assert res.status_code==404, res.status_code


