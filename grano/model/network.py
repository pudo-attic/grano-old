from datetime import datetime

from grano.core import db
from grano.model import util

class Network(db.Model):
    __tablename__ = 'network'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Unicode)
    title = db.Column(db.Unicode)

    description = db.Column(db.Unicode)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @property
    def entities(self):
        return self.all_entities.filter_by(current=True)

    @property
    def relations(self):
        return self.all_relations.filter_by(current=True)

    def as_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'num_entities': self.entities.count(),
            'num_relations': self.relations.count(),
            }

    @classmethod
    def by_id(self, id):
        q = db.session.query(Network)
        q = q.filter_by(id=id)
        return q.first()

    @classmethod
    def by_slug(self, slug):
        q = db.session.query(Network)
        q = q.filter_by(slug=slug)
        return q.first()

    def __repr__(self):
        return "<Network(%s,%s)>" % (self.id, self.slug)


