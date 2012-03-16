from flaskext.script import Manager

from grano.core import app, db
from grano.model import *

manager = Manager(app)

@manager.command
def createdb():
    """ Create the SQLAlchemy database. """
    db.create_all()

@manager.command
def sqlshell(network):
    import sys
    from grano.model import Network
    from pprint import pprint
    network = Network.by_slug(network)
    print network
    while True:
        sys.stdout.write("%s> " % network.slug)
        command = sys.stdin.readline()
        try:
            rp = network.raw_query(command)
            pprint(rp.fetchall())
        except Exception, e:
            print e
            #raise


if __name__ == '__main__':
    manager.run()
