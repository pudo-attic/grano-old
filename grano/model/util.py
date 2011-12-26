from uuid import uuid4
from time import time



def make_id():
    return unicode(uuid4())

def make_serial():
    return int(time()*1000)


