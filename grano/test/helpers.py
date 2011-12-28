from grano.core import app, db
from grano import core, web

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
            }
        }
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

def skip(*args, **kwargs):
    raise SkipTest(*args, **kwargs)

def make_test_app(use_cookies=False):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all()
    return app.test_client(use_cookies=use_cookies)

def tear_down_test_app():
    db.session.rollback()
    db.drop_all()
