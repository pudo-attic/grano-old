from datetime import datetime

from grano.core import db
from grano.model import util

class Entity(db.Model):
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
    
    def __repr__(self):
        return "<Entity:%s(%s,%s)>" % (self.type, self.id, self.slug)

