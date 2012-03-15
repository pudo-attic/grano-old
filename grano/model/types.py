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
        serial = db.Column(db.BigInteger, primary_key=True, default=util.make_serial)
        type = db.Column(db.Unicode)

        __mapper_args__ = {'polymorphic_on': type}
        __table_args__ = {'extend_existing': True}

        current = db.Column(db.Boolean)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        slug = db.Column(db.Unicode)
        title = db.Column(db.Unicode)

        def update_values(self, schema, data):
            self.title = data.get('title')
            self.slug = util.slugify(self.title)

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
                'created_at': self.created_at
                }

        def as_deep_dict(self):
            data = self.as_dict()
            data['incoming'], data['outgoing'] = [], []
            for rel in self.incoming:
                reldata = rel.as_dict()
                reldata['source'] = rel.source.as_dict()
                data['incoming'].append(reldata)
            for rel in self.outgoing:
                reldata = rel.as_dict()
                reldata['target'] = rel.source.as_dict()
                data['outgoing'].append(reldata)
            return data

        def __repr__(self):
            return "<Entity:%s(%s,%s)>" % (self.type, self.id, self.slug)

    class Relation(db.Model, RevisionedMixIn, ViewMixIn):
        """ Edge data type. This is never instantiated directly, only through a
        schema definition which will create a joined subtype. """

        __tablename__ = relation_table_name
        id = db.Column(db.String(36), primary_key=True, default=util.make_id)
        serial = db.Column(db.BigInteger, primary_key=True,
            default=util.make_serial)
        type = db.Column(db.Unicode)

        __mapper_args__ = {'polymorphic_on': type}
        __table_args__ = {'extend_existing': True}

        current = db.Column(db.Boolean)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

        source_id = db.Column(db.String(36))
        target_id = db.Column(db.String(36))

        def update_values(self, schema, data):
            self.source_id = data.get('source').id
            self.target_id = data.get('target').id

        def as_dict(self):
            return {
                'id': self.id,
                'serial': self.serial,
                'type': self.type,
                'current': self.current,
                'created_at': self.created_at,
                'source': self.source_id,
                'target': self.target_id
                }

        def as_deep_dict(self):
            data = self.as_dict()
            data['source'] = self.source.as_dict()
            data['target'] = self.target.as_dict()
            return data

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

    Entity.metadata = network.meta
    Entity.__table__.metadata = network.meta
    Relation.metadata = network.meta
    Relation.__table__.metadata = network.meta

    return Entity, Relation
