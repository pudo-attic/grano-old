import unittest
import json

from grano import core
from grano import model
from grano import web

NETWORK_FIXTURE = {'title': 'The One Percent', 
                   'description': 'A very neat resource!'}

from grano.test.helpers import make_test_app, tear_down_test_app

class NetworkAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = make_test_app()
        self.make_fixtures()

    def tearDown(self):
        tear_down_test_app()

    def make_fixtures(self):
        #self.app.post('/api/v1/resource/fixture', 
        #              data=RESOURCE_FIXTURE,
        #              headers={'Authorization': AUTHZ})
        pass

    def test_network_index(self):
        res = self.app.get('/api/1/networks')
        body = json.loads(res.data)
        assert len(body)==0, body

    def test_network_create(self):
        assert False
