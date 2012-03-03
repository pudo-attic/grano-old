from datetime import datetime
from hashlib import sha1
import os

from grano.core import db


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    fullname = db.Column(db.Unicode)
    email = db.Column(db.Unicode)
    _password = db.Column('password', db.Unicode)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def _set_password(self, password):
        """Hash password on the fly."""
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(salt.hexdigest() + password_8bit)
        hashed_password = salt.hexdigest() + hash.hexdigest()

        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self._password = hashed_password

    def _get_password(self):
        """Return the password hashed"""
        return self._password

    password = db.synonym('_password', \
        descriptor=property(_get_password, _set_password))

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hashed_pass = sha1()
        hashed_pass.update(self._password[:40] + password)
        return self._password[40:] == hashed_pass.hexdigest()

    @classmethod
    def create(cls, data):
        obj = cls()
        obj.name = data.get('name')
        obj.update(data)
        return obj

    def update(self, data):
        self.fullname = data.get('fullname')
        self.email = data.get('email')
        self.password = data.get('password')
        db.session.add(self)
        db.session.flush()

    @property
    def display_name(self):
        return self.fullname or self.name

    def get_id(self):
        return unicode(self.name)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'fullname': self.fullname,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            }

    @classmethod
    def by_name(self, name):
        q = db.session.query(Account)
        q = q.filter_by(name=name)
        return q.first()

    def __repr__(self):
        return '<Account(%r)>' % (self.name)
