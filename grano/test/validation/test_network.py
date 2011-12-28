import unittest
from pprint import pprint
from datetime import datetime
from copy import deepcopy

from colander import Invalid

from grano.model import Network
from grano.core import db
from grano.test import helpers as h
from grano.validation.network import validate_network
from grano.validation.types import ValidationContext

TEST_NETWORK = {
    'title': 'My Network',
    'description': 'This is a test',
    }

class TestNetworkValidation(unittest.TestCase):

    def setUp(self):
        self.client = h.make_test_app()
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
            context = ValidationContext()
            validate_network(TEST_NETWORK, context)
        except Invalid, i:
            assert False, i.asdict()

    @h.raises(Invalid)
    def test_no_title(self):
        in_ = deepcopy(TEST_NETWORK)
        del in_['title']
        context = ValidationContext()
        validate_network(in_, context)
        
    @h.raises(Invalid)
    def test_existing_slug(self):
        in_ = deepcopy(TEST_NETWORK)
        in_['slug']='net'
        context = ValidationContext()
        validate_network(in_, context)
