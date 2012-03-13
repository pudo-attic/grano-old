from datetime import datetime
from itertools import chain

from grano.core import db
from grano.model.types import make_types
from grano.model.schema import Schema


class Network(db.Model):
    __tablename__ = 'network'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Unicode)
    title = db.Column(db.Unicode)

    description = db.Column(db.Unicode)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def _ensure_types(self):
        if not hasattr(self, '_Entity'):
            self._Entity, self._Relation = make_types(self)

    @db.reconstructor
    def reconstruct(self):
        # map these into the ORM
        [rs.cls for rs in self.relation_schemata]
        [es.cls for es in self.entity_schemata]

    @property
    def Entity(self):
        self._ensure_types()
        return self._Entity

    @property
    def Relation(self):
        self._ensure_types()
        return self._Relation

    @property
    def all_entities(self):
        return db.query(self.Entity)

    @property
    def all_relations(self):
        return db.query(self.Relation)

    @property
    def entities(self):
        return self.all_entities.filter_by(current=True)

    @property
    def relations(self):
        return self.all_relations.filter_by(current=True)

    @property
    def entity_schemata(self):
        return self.schemata.filter_by(entity=Schema.ENTITY)

    def get_entity_schema(self, name):
        return self.entity_schemata.filter_by(name=name).first()

    @property
    def relation_schemata(self):
        return self.schemata.filter_by(entity=Schema.RELATION)

    def get_relation_schema(self, name):
        return self.relation_schemata.filter_by(name=name).first()

    @classmethod
    def create(cls, data):
        obj = cls()
        obj.update(data)
        #bind = db.session.bind
        #bind = obj.__table__.bind
        #bind = db.engine
        #import ipdb; ipdb.set_trace()
        #print bind
        #if not obj.Entity.__table__.exists(bind):
        #    obj.Entity.__table__.create(bind)
        #if not obj.Relation.__table__.exists(bind):
        #    obj.Relation.__table__.create(bind)
        return obj

    def update(self, data):
        self.title = data.get('title')
        self.slug = data.get('slug')
        self.description = data.get('description')
        db.session.add(self)
        db.session.flush()

    def delete(self):
        self.deleted_at = datetime.utcnow()

    def as_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            #'num_entities': self.entities.count(),
            #'num_relations': self.relations.count(),
            }

    def raw_query(self, query, *a, **kw):
        conn = db.engine.connect()
        true = db.Boolean().bind_processor(db.engine.dialect)(True)
        for rs in chain(self.relation_schemata, self.entity_schemata):
            q = rs.cls.view().replace("?", str(true))
            conn.execute(q)
        return conn.execute(query, *a, **kw)


    @classmethod
    def by_id(self, id):
        q = db.session.query(Network)
        q = q.filter_by(id=id)
        q = q.filter_by(deleted_at=None)
        return q.first()

    @classmethod
    def by_slug(self, slug):
        q = db.session.query(Network)
        q = q.filter_by(slug=slug)
        q = q.filter_by(deleted_at=None)
        return q.first()

    @classmethod
    def all(self):
        q = db.session.query(Network)
        q = q.filter_by(deleted_at=None)
        return q

    def __repr__(self):
        return "<Network(%s,%s)>" % (self.id, self.slug)
