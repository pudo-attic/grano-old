from flaskext.script import Manager

from grano.core import app, db
from grano.model import *

manager = Manager(app)

@manager.command
def createdb():
    """ Create the SQLAlchemy database. """
    db.create_all()
    p = Person()
    p.title = "Foo"
    p.current = True
    db.session.add(p)
    db.session.flush()
    b = Person()
    b.title = "Bar"
    b.current = True
    db.session.add(b)
    db.session.flush()
    r = Social()
    r.source_id = p.id
    r.target_id = b.id
    r.current = True
    print r.source
    db.session.add(r)
    db.session.commit()

    for rel in Relation.query.all():
        print rel.target
        print rel.source



if __name__ == '__main__':
    manager.run()
