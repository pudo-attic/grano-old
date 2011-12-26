from grano.core import app, db

def make_test_app(use_cookies=False):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all()
    return app.test_client(use_cookies=use_cookies)

def tear_down_test_app():
    db.session.rollback()
    db.drop_all()
