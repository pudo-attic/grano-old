from grano.core import db

ATTRIBUTE_TYPES_DB = {
    'string': db.Unicode,
    'float': db.Float,
    'integer': db.Integer,
    'date': db.DateTime
    }

class SchemaSet(object):
    pass

class Schema(object):

    def __init__(self, parent_cls, data):
        self.parent_cls = parent_cls
        self.name = data['name']
        self.label = data['label']
        self.attributes = []
        self._cls = None
        for name, adata in data['attributes'].items():
            self.attributes.append(Attribute(name, adata))

    @property
    def cls(self):
        if self._cls is None:
            self._cls = self._make_cls()
        return self._cls

    def _make_cls(self):
        prefix = self.parent_cls.__tablename__
        cls = {
            '__tablename__': prefix + '_' + self.name,
            'id': db.Column(db.String(36), db.ForeignKey(prefix + '.id'),
                primary_key=True),
            'serial': db.Column(db.Integer, db.ForeignKey(prefix + '.serial'),
                primary_key=True)
            }
        cls['__mapper_args__'] = {
                'polymorphic_identity': self.name,
                'inherit_condition': db.and_(
                    cls['id']==self.parent_cls.id,
                    cls['serial']==self.parent_cls.serial)
                }
        for attribute in self.attributes:
            cls[attribute.name] = db.Column(attribute.column_type)
        return type(self.name, (self.parent_cls,), cls)


class Attribute(object):

    def __init__(self, name, data):
        self.name = name
        self.type = data['type']
        self.label = data['label']
        self.help = data['help']

    @property
    def column_type(self):
        return ATTRIBUTE_TYPES_DB[self.type]

