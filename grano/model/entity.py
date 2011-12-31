from datetime import datetime

from grano.core import db
from grano.model import util
from grano.model.revision import RevisionedMixIn

class Entity(db.Model, RevisionedMixIn):
    """ Node type, never really instantiated directly. """

    __tablename__ = 'entity'
    id = db.Column(db.String(36), primary_key=True, default=util.make_id)
    serial = db.Column(db.Integer, primary_key=True, default=util.make_serial)
    type = db.Column(db.Unicode)

    incoming = db.relationship('Relation', lazy='dynamic',
            primaryjoin='(Relation.target_id==Entity.id) & (Relation.current==True)',
            foreign_keys=[id],
            backref=db.backref('target', uselist=False,
                primaryjoin='(Relation.target_id==Entity.id) & (Entity.current==True)'))
    outgoing = db.relationship('Relation', lazy='dynamic',
            primaryjoin='(Relation.source_id==Entity.id) & (Relation.current==True)',
            foreign_keys=[id],
            backref=db.backref('source', uselist=False,
                primaryjoin='(Relation.source_id==Entity.id) & (Entity.current==True)'))

    __mapper_args__ = {'polymorphic_on': type}

    current = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.Unicode)
    title = db.Column(db.Unicode)
    
    summary = db.Column(db.Unicode)
    description = db.Column(db.Unicode)

    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    network = db.relationship('Network',
        backref=db.backref('all_entities', lazy='dynamic'))
    
    def update_values(self, schema, data):
        self.title = data.get('title')
        self.slug = util.slugify(self.title)
        self.summary = data.get('summary')
        self.description = data.get('description')
        self.network = data.get('network')

    def delete(self, schema):
        super(Entity, self).delete(schema)
        # TODO: how to get relation schemata?
        #for relation in self.incoming:
        #    relation.delete()

    def as_dict(self):
        return {
            'id': self.id,
            'serial': self.serial,
            'type': self.type,
            'current': self.current,
            'slug': self.slug,
            'title': self.title,
            'created_at': self.created_at,
            'summary': self.summary,
            'description': self.description,
            'network': self.network.slug if self.network else None
            }

    def __repr__(self):
        return "<Entity:%s(%s,%s)>" % (self.type, self.id, self.slug)

