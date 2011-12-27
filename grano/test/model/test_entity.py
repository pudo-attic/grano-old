import unittest
from grano.core import db
from grano.test import helpers as h
from grano.model.network import Network
from grano.model.entity import Entity
from grano.model.schema import Schema

class TestEntity(unittest.TestCase):

    def setUp(self):
        self.network = Network()
        self.network.title = 'Net'
        self.network.slug = 'net'
        self.client = h.make_test_app()

    def tearDown(self):
        h.tear_down_test_app()

    def test_basic_entity(self):
        entity = Entity()
        entity.network = self.network
        entity.title = "Foo"
        assert entity.as_dict()['title']=='Foo'

    def test_entity_schema(self):
        schema = Schema(Entity, h.TEST_ENTITY_SCHEMA)
        obj = schema.cls()
        obj.birth_place = 'Utopia'
        obj.title = 'The Man'
        obj.slug = 'the-man'
        db.session.add(obj)
        db.session.flush()
        assert obj.id!=None
        assert obj.serial!=None


