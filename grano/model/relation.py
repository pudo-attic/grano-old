from datetime import datetime

from grano.core import db
from grano.model import util
from grano.model.revision import RevisionedMixIn

class Relation(db.Model, RevisionedMixIn):
    """ Edge data type. This is never instantiated directly, only through a 
    schema definition which will create a joined subtype. """

    __tablename__ = 'relation'
    id = db.Column(db.String(36), primary_key=True, default=util.make_id)
    serial = db.Column(db.Integer, primary_key=True, default=util.make_serial)
    type = db.Column(db.Unicode)
    
    __mapper_args__ = {'polymorphic_on': type}

    current = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    source_id = db.Column(db.String(36), db.ForeignKey('entity.id'))
    target_id = db.Column(db.String(36), db.ForeignKey('entity.id'))

    network = db.relationship('Network',
        backref=db.backref('all_relations', lazy='dynamic'))
    
    def update_values(self, schema, data):
        # TODO: source
        # TODO: target
        # TODO: network
        pass

    def as_dict(self):
        return {
            'id': self.id,
            'serial': self.serial,
            'type': self.type,
            'current': self.current,
            'created_at': self.created_at,
            'network': self.network.slug,
            'source': self.source_id,
            'target': self.target_id
            }

    def __repr__(self):
        return "<Relation:%s(%s,%s,%s)>" % (self.type, self.id,
                self.source_id, self.target_id)

