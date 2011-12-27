from grano.core import db
from grano.model.util import make_serial

class RevisionedMixIn(object):
    """ Simple versioning system for the database graph objects.
    This is based upon multiple objects sharing the smae ID, but
    differing in their serial number. Additionally, a ``current``
    flag is used to flag that revision of a given edge or node 
    that should currently be used. """

    @classmethod
    def create(cls, schema, data):
        """ Create a new, versioned object. """
        obj = schema.cls()
        obj._update(schema, data)
        return obj
    
    def update(self, schema, data, current=True):
        """ Create a new object as a child of an existing, 
        versioned object while changing the serial number to 
        differentiate the child. """
        obj = schema.cls()
        obj.id = self.id
        data_ = self.as_dict()
        data_.update(data)
        obj._update(schema, data_)
        return obj

    def _update(self, schema, data, current=True):
        for attribute in schema.attributes:
            setattr(self, attribute.name, 
                data.get(attribute.name))
        self.update_values(schema, data)
        self.serial = make_serial()
        self.type = schema.name
        if current:
            # this is slightly hacky but it cannot 
            # be assumed that the `current` version
            # is the parent object to the new obj.
            table = schema.parent_cls.__table__
            q = table.update().where(table.c.id==self.id)
            q = q.values({'current': False})
            db.session.execute(q)
            self.current = True
        db.session.add(self)
        db.session.flush()

    def update_values(self, schema, data):
        raise TypeError()

    @classmethod
    def current_by_id(cls, id):
        q = db.session.query(cls)
        q = q.filter_by(current=True)
        q = q.filter_by(id=id)
        return q.first()

    @classmethod
    def all(cls):
        q = db.session.query(cls)
        q = q.filter_by(current=True)
        return q



