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
        'shoe_size': {
            'type': 'integer',
            'label': 'Shoe Size',
            'help': 'European shoe size',
            'missing': 40
            },
        'birth_place': {
            'type': 'string',
            'label': 'Birth Place',
            'help': 'The place of birth.'
            },
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

TEST_USER = {
    'name': 'hugo',
    'fullname': 'Hungry Hugo',
    'email': 'hungry@hugo.org',
    'password': 'foo'
    }

AUTHZ = '%s:%s' % (TEST_USER['name'], TEST_USER['password'])
AUTHZ_HEADER = {'Authorization': 'Basic ' + AUTHZ.encode('base64').strip()}


def skip(*args, **kwargs):
    raise SkipTest(*args, **kwargs)


def make_test_app(use_cookies=False):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    #import ipdb; ipdb.set_trace()
    from grano.model import Account
    db.create_all()
    client = app.test_client(use_cookies=use_cookies)
    app.test_user = Account.create(TEST_USER)
    db.session.commit()
    return client


def tear_down_test_app():
    db.session.rollback()
    db.drop_all()
