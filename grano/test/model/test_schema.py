import unittest
from grano.test import helpers 

class TestSchema(unittest.TestCase):

    def setUp(self):
        self.client = helpers.make_test_app()

    def tearDown(self):
        helpers.tear_down_test_app()

    def test_basic_schema(self):
        assert True

