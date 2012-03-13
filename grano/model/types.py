from datetime import datetime
from sqlalchemy.sql import select

from grano.core import db
from grano.model import util
from grano.model.revision import RevisionedMixIn


class ViewMixIn(object):

    @classmethod
    def view(cls):
        """ Create a temporary view to simplify queries against the
        data model. """
        parent_cls = cls.__bases__[0]
        parent_table = parent_cls.__table__
        table = cls.__table__
        view_name = '%s_%s' % (parent_cls.__name__.lower(),
                               cls.__name__)
        columns = table.columns + parent_table.columns
        columns = [c for c in columns if c not in (table.c.id, table.c.serial)]
        columns = [c.label(c.name) for c in columns]
        q = select(columns,
            db.and_(parent_table.c.id == table.c.id,
                    parent_table.c.serial == table.c.serial,
                    parent_table.c.current == True))
        return 'CREATE TEMP VIEW %s AS %s' % (view_name, q)


def make_types(network):
    relation_table_name = network.slug + '__relation'
    entity_table_name = network.slug + '__entity'

#    entity_table = db.metadata.tables.get(entity_table_name)
#    relation_table = db.metadata.tables.get(relation_table_name)

    class Entity(db.Model, RevisionedMixIn, ViewMixIn):
        """ Node type, never really instantiated directly. """

        __tablename__ = entity_table_name
        id = db.Column(db.String(36), primary_key=True, default=util.make_id)
        serial = db.Column(db.Integer, primary_key=True,
            default=util.make_serial)
        type = db.Column(db.Unicode)

        __mapper_args__ = {'polymorphic_on': type}
        __table_args__ = {'extend_existing': True}

        current = db.Column(db.Boolean)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        slug = db.Column(db.Unicode)
        title = db.Column(db.Unicode)

        summary = db.Column(db.Unicode)
        description = db.Column(db.Unicode)

        network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
        network = db.relationship('Network')

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

    class Relation(db.Model, RevisionedMixIn, ViewMixIn):
        """ Edge data type. This is never instantiated directly, only through a
        schema definition which will create a joined subtype. """

        __tablename__ = relation_table_name
        id = db.Column(db.String(36), primary_key=True, default=util.make_id)
        serial = db.Column(db.Integer, primary_key=True,
            default=util.make_serial)
        type = db.Column(db.Unicode)

        __mapper_args__ = {'polymorphic_on': type}
        __table_args__ = {'extend_existing': True}

        current = db.Column(db.Boolean)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

        network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
        source_id = db.Column(db.String(36),
                db.ForeignKey(entity_table_name + '.id'))
        target_id = db.Column(db.String(36),
                db.ForeignKey(entity_table_name + '.id'))

        network = db.relationship('Network')

        def update_values(self, schema, data):
            self.source_id = data.get('source').id
            self.target_id = data.get('target').id
            self.network = data.get('network')

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

    Entity.incoming = db.relationship(Relation, lazy='dynamic',
                primaryjoin=db.and_(Relation.target_id==Entity.id, Relation.current==True),
                foreign_keys=[Entity.id],
                backref=db.backref('target', uselist=False,
                    primaryjoin=db.and_(Relation.target_id==Entity.id, Entity.current==True)))
    Entity.outgoing = db.relationship(Relation, lazy='dynamic',
                primaryjoin=db.and_(Relation.source_id==Entity.id, Relation.current==True),
                foreign_keys=[Entity.id],
                backref=db.backref('source', uselist=False,
                    primaryjoin=db.and_(Relation.source_id==Entity.id, Entity.current==True)))

#    if entity_table:
#        Entity.__table__ = entity_table
    #import ipdb; ipdb.set_trace()
#    if Entity.__tablename__ in db.metadata.tables:
#        Entity.__table__ = db.metadata.tables[Entity.__tablename__]
#    
#    if Relation.__tablename__ in db.metadata.tables:
#        Relation.__table__ = db.metadata.tables[Relation.__tablename__]

    return Entity, Relation
