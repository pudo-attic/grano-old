import colander
from datetime import datetime

from grano.core import db


ATTRIBUTE_TYPES_DB = {
    'string': db.Unicode,
    'float': db.Float,
    'integer': db.Integer,
    'date': db.DateTime
    }


class Schema(db.Model):
    """ A schema defines a specific subtype of either an entity or a relation.
    This can mean any graph element, such as a person, company or other actor
    type for entities - or a type of social, economic or political link for a 
    relation (e.g. ownership, school attendance, ..).

    A schema is defined through a model structure that contains necessary 
    metadata to handle the schema both internally and via the user interface.
    """
    __tablename__ = 'schema'

    ENTITY = 'entity'
    RELATION = 'relation'
    TYPES = [ENTITY, RELATION]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    label = db.Column(db.Unicode)
    entity = db.Column(db.Unicode)

    network_id = db.Column(db.Integer, db.ForeignKey('network.id'))
    network = db.relationship('Network',
        backref=db.backref('schemata', lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @classmethod
    def create(cls, network, entity, data):
        obj = cls()
        obj.update(network, entity, data)
        return obj

    def update(self, network, entity, data):
        self.network = network
        self.name = str(data.get('name'))
        self.label = data.get('label')
        self.entity = entity
        db.session.add(self)
        db.session.flush()
        remaining = []
        for name, data in data.get('attributes', {}).items():
            remaining.append(name)
            attr = Attribute.create(name, data)
            self.attributes.append(attr)
        for attribute in self.attributes:
            if not attribute.name in remaining:
                attribute.delete()
        db.session.flush()
        self.migrate()

    def migrate(self):
        self._make_cls()
        parent_table = self.parent_cls.__table__
        if not parent_table.exists():
            parent_table.create()
        table = self._cls.__table__
        if not table.exists():
            table.create()
        for attribute in self.attributes:
            try:
                col = table.c[attribute.name]
                col.create()
            except:
                pass

    def delete(self):
        for attribute in self.attributes:
            attribute.delete()
        db.session.delete(self)

    @property
    def cls(self):
        if not hasattr(self, '_cls'):
            self._make_cls()
        return self._cls

    @property
    def parent_cls(self):
        return {
            self.ENTITY: self.network.Entity,
            self.RELATION: self.network.Relation,
            }.get(self.entity)

    def _make_cls(self):
        """ Generate a new type, mapped through SQLAlchemy. This will be a
        joined subtable to either an entity or a relation and retain a copy
        of its composite primary key plus any attributes defined in the
        schema. """
        prefix = self.parent_cls.__tablename__

        # inherit primary key:
        cls = {
            '__tablename__': prefix + '__' + self.name,
            'id': db.Column(db.String(36), db.ForeignKey(prefix + '.id'),
                primary_key=True),
            'serial': db.Column(db.Integer, db.ForeignKey(prefix + '.serial'),
                primary_key=True)
            }

        # set up inheritance:
        cls['__mapper_args__'] = {
                'polymorphic_identity': self.name,
                'inherit_condition': db.and_(
                    cls['id'] == self.parent_cls.id,
                    cls['serial'] == self.parent_cls.serial)
                }
        cls['__table_args__'] = {
                'extend_existing': True
                }

        # set up the specific attributes:
        for attribute in self.attributes:
            cls[attribute.name] = attribute.column

        # make an as_dict method:
        def as_dict(ins):
            d = self.parent_cls.as_dict(ins)
            for attribute in self.attributes:
                d[attribute.name] = \
                    getattr(ins, attribute.name)
            return d
        cls['as_dict'] = as_dict

        self._cls = type(str(self.name), (self.parent_cls,), cls)
        table = self._cls.__table__
        if table.name in db.metadata.tables:
            table.metadata.remove(table)
        table.metadata.bind = db.engine

    def as_dict(self):
        attrs = [(a.name, a.as_dict()) for a in self.attributes]
        return {
            'id': self.id,
            'name': self.name,
            'label': self.label,
            'entity': self.entity,
            'attributes': dict(attrs)
            }

    def __repr__(self):
        return "<Schema(%s,%s)>" % (self.id, self.name)


class Attribute(db.Model):
    """ Attributes are specific properties of a schema for either an entity or 
    a relation. They materialize as columns on the joined sub-table for the 
    schema. """
    __tablename__ = 'schema_attribute'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    label = db.Column(db.Unicode)
    type = db.Column(db.Unicode)
    help = db.Column(db.Unicode)
    missing = db.Column(db.Unicode)

    schema_id = db.Column(db.Integer, db.ForeignKey('schema.id'))
    schema = db.relationship(Schema,
        backref=db.backref('attributes', lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @classmethod
    def create(cls, name, data):
        obj = cls()
        obj.update(name, data)
        return obj

    def update(self, name, data):
        self.name = name
        self.label = data.get('label')
        self.type = data.get('type')
        self.help = data.get('help')
        self.missing = data.get('missing')
        db.session.add(self)
        db.session.flush()

    def delete(self):
        db.session.delete(self)

    def as_dict(self):
        return {
            'label': self.label,
            'type': self.type,
            'help': self.help,
            'missing': self.missing
            }

    @property
    def column(self):
        # TODO: do we also need some typecasting mechanism?
        type_ = ATTRIBUTE_TYPES_DB[self.type]
        return db.Column(self.name, type_)

    def __repr__(self):
        return "<Attribute(%s,%s)>" % (self.id, self.name)



