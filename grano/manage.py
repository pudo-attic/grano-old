from flaskext.script import Manager

from grano.core import app, db
from grano.model import *

manager = Manager(app)

@manager.command
def createdb():
    """ Create the SQLAlchemy database. """
    db.create_all()

if __name__ == '__main__':
    manager.run()
