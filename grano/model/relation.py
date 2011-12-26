from datetime import datetime

from grano.core import db
from grano.model import util

class Relation(db.Model):
    __tablename__ = 'relation'
    id = db.Column(db.String(36), primary_key=True, default=util.make_id)
    serial = db.Column(db.Integer, primary_key=True, default=util.make_serial)
    type = db.Column(db.Unicode)
    
    source_id = db.Column(db.String(36), db.ForeignKey('entity.id'))
    target_id = db.Column(db.String(36), db.ForeignKey('entity.id'))

    __mapper_args__ = {'polymorphic_on': type}

    current = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Social(Relation):
    __tablename__ = 'relation_social'
    id = db.Column(db.String(36), db.ForeignKey('relation.id'), primary_key=True)
    serial = db.Column(db.Integer, db.ForeignKey('relation.serial'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'social',
            'inherit_condition': db.and_(id==Relation.id, serial==Relation.serial)}

    link_type = db.Column(db.Unicode)

