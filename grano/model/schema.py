from grano.core import db

ATTRIBUTE_TYPES_DB = {
    'string': db.Unicode,
    'float': db.Float,
    'integer': db.Integer,
    'date': db.DateTime
    }

class SchemaSet(dict):
    
    def add(self, schema):
        self[schema.name] = schema


class Schema(object):
    """ A schema defines a specific subtype of either an entity or a relation.
    This can mean any graph element, such as a person, company or other actor
    type for entities - or a type of social, economic or political link for a 
    relation (e.g. ownership, school attendance, ..).

    A schema is defined through a model structure that contains necessary 
    metadata to handle the schema both internally and via the user interface.
    """

    def __init__(self, parent_cls, data):
        self.parent_cls = parent_cls
        self.name = str(data['name'])
        self.label = data['label']
        self.attributes = []
        self._cls = None
        for name, adata in data['attributes'].items():
            self.attributes.append(Attribute(name, adata))

    @property
    def cls(self):
        if self._cls is None:
            self._cls = self._make_cls()
            table = self._cls.__table__
            if table.name in db.metadata.tables:
                table.metadata.remove(table)
            table.metadata.bind = db.engine
            if not table.exists():
                table.create()
        return self._cls

    def _make_cls(self):
        """ Generate a new type, mapped through SQLAlchemy. This will be a 
        joined subtable to either an entity or a relation and retain a copy
        of its composite primary key plus any attributes defined in the 
        schema. """
        prefix = self.parent_cls.__tablename__

        # inherit primary key:
        cls = {
            '__tablename__': prefix + '_' + self.name,
            'id': db.Column(db.String(36), db.ForeignKey(prefix + '.id'),
                primary_key=True),
            'serial': db.Column(db.Integer, db.ForeignKey(prefix + '.serial'),
                primary_key=True)
            }

        # set up inheritance:
        cls['__mapper_args__'] = {
                'polymorphic_identity': self.name,
                'inherit_condition': db.and_(
                    cls['id']==self.parent_cls.id,
                    cls['serial']==self.parent_cls.serial)
                }

        # set up the specific attributes:
        for attribute in self.attributes:
            cls[attribute.name] = db.Column(attribute.column_type)

        # make an as_dict method:
        def as_dict(ins):
            d = self.parent_cls.as_dict(ins)
            for attribute in self.attributes:
                d[attribute.name] = \
                    getattr(ins, attribute.name)
            return d
        cls['as_dict'] = as_dict

        return type(self.name, (self.parent_cls,), cls)


class Attribute(object):
    """ Attributes are specific properties of a schema for either an entity or 
    a relation. They materialize as columns on the joined sub-table for the 
    schema. """

    def __init__(self, name, data):
        self.name = name
        self.type = data['type']
        self.label = data['label']
        self.help = data.get('help')

    @property
    def column_type(self):
        # TODO: do we also need some typecasting mechanism?
        return ATTRIBUTE_TYPES_DB[self.type]

