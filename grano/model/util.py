import re
from uuid import uuid4
from time import time
from unidecode import unidecode
from datetime import datetime
from json import dumps, loads
from sqlalchemy import sql
from sqlalchemy.types import Text, MutableType, TypeDecorator, \
    UserDefinedType

SLUG_RE = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delimiter='-'):
    '''\
    Generate an ascii only slug from the text that can be
    used in urls or as a name.
    '''
    result = []
    for word in SLUG_RE.split(unicode(text).lower()):
        result.extend(unidecode(word).split())
    return unicode(delimiter.join(result))


def make_id():
    return unicode(uuid4())


def make_serial():
    return int(time() * 1000)


def graph_values(d):
    for k, v in d.items():
        if k == 'type':
            d['_type'] = d['type']
        if v is None or k == 'type':
            del d[k]
        elif isinstance(v, datetime):
            d[k] = v.isoformat()
        else:
            d[k] = unicode(v)
    return d


class TSVector(UserDefinedType):
    """Support for PostgreSQL full-text search."""

    def get_col_spec(self):
        from grano.core import db
        if db.engine.dialect.name == 'postgresql':
            return 'tsvector'
        return 'text'

    @classmethod
    def make_text(cls, bind, text):
        if bind.engine.dialect.name == 'postgresql':
            return sql.select([sql.func.to_tsvector(text)], bind=bind).scalar()
        return text


class JSONType(MutableType, TypeDecorator):
    impl = Text

    def __init__(self):
        super(JSONType, self).__init__()

    def process_bind_param(self, value, dialect):
        return dumps(value)

    def process_result_value(self, value, dialiect):
        return loads(value)

    def copy_value(self, value):
        return loads(dumps(value))
