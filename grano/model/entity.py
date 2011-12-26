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


class Person(Entity):
    __tablename__ = 'entity_person'
    id = db.Column(db.String(36), db.ForeignKey('entity.id'), primary_key=True)
    serial = db.Column(db.Integer, db.ForeignKey('entity.serial'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'person',
            'inherit_condition': db.and_(id==Entity.id, serial==Entity.serial)}

    birth_place = db.Column(db.Unicode)
