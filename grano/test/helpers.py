from grano.core import app, db
from grano import core, web
from grano.model import schema_registry

from nose.tools import *
from nose.plugins.skip import SkipTest

TEST_ENTITY_SCHEMA = {
    'name': 'person',
    'label': 'Person',
    'attributes': {
        'birth_day': {
            'type': 'date',
            'label': 'Birth Day',
            'help': 'The person\'s birth day.'
            },
        'death_day': {
            'type': 'date',
            'label': 'Death Day',
            'help': 'The day the person died.'
            },
        'birth_place': {
            'type': 'string',
            'label': 'Birth Place',
            'help': 'The place of birth.'
            },
        'shoe_size': {
            'type': 'integer',
            'label': 'Shoe Size',
            'help': 'European shoe size',
            'missing': 40
            }
        },
    }

TEST_RELATION_SCHEMA = {
    'name': 'social',
    'label': 'Social Connection',
    'attributes': {
        'link_type': {
            'type': 'string',
            'label': 'Link Type',
            }
        }
    }

TEST_SCHEMA = {'entity': [TEST_ENTITY_SCHEMA], 'relation': [TEST_RELATION_SCHEMA]}

def skip(*args, **kwargs):
    raise SkipTest(*args, **kwargs)

def make_test_app(use_cookies=False):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all()
    return app.test_client(use_cookies=use_cookies)

def load_registry():
    from grano.validation.schema_loader import SchemaLoader
    SchemaLoader.load_data(schema_registry, TEST_SCHEMA)

def tear_down_test_app():
    db.session.rollback()
    db.drop_all()
