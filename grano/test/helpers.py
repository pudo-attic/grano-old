from grano.core import web, db

def make_test_app(use_cookies=False):
    web.app.config['TESTING'] = True
    web.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all()
    return web.app.test_client(use_cookies=use_cookies)

def tear_down_test_app():
    db.session.rollback()
    db.drop_all()
