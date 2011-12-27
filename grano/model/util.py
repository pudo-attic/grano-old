import re
from uuid import uuid4
from time import time
from unidecode import unidecode

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
    return int(time()*1000)


