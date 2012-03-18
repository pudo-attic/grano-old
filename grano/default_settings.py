DEBUG = True
SECRET_KEY = 'no'
SITE_TITLE = 'lobbytransparency.eu'
REGISTRATION = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///grano.db'
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/grano_lobby'


# HACK HACK - Need a proper mechanism for this.
STORED_QUERIES = {
    'test': {
        'label': 'Test Query',
        'query': 'SELECT * FROM entity_actor'
        }
    }
