import logging
from datetime import datetime
from itertools import chain

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import text

from grano.core import db


log = logging.getLogger(__name__)


def safe_engine():
    from grano.core import app
    # TODO: put in read-only conn string.
    uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    return create_engine(uri)


class Query(db.Model):
    """
    A query object is a stored raw query to be run against the
    network to generate a report.
    """
    __tablename__ = 'query'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    label = db.Column(db.Unicode)
    query = db.Column(db.Unicode)

    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    network = db.relationship('Network',
        backref=db.backref('queries', lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @classmethod
    def create(cls, network, data):
        obj = cls()
        obj.network = network
        obj.update(data)
        return obj

    def update(self, data):
        self.name = str(data.get('name'))
        self.label = data.get('label')
        self.query = data.get('query')
        db.session.add(self)
        db.session.flush()

    def delete(self):
        db.session.delete(self)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'label': self.label,
            'query': self.query
            }

    def run(self, **kw):
        conn = safe_engine().connect()
        for rs in chain(self.network.relation_schemata,
            self.network.entity_schemata):
            q = rs.cls.view()
            conn.execute(text(str(q)), current=True)
        return conn.execute(text(self.query), **kw)

    @classmethod
    def by_name(self, network, name):
        q = db.session.query(Query)
        q = q.filter_by(network=network)
        q = q.filter_by(name=name)
        return q.first()

    @classmethod
    def all(self, network):
        q = db.session.query(Query)
        q = q.filter_by(network=network)
        return q

    def __repr__(self):
        return "<Query(%s,%s)>" % (self.id, self.name)
