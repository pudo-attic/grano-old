import re

from colander import SchemaNode, Function, String
from colander import Mapping, Sequence


def _node(schema, name, *children, **kw):
    if 'validator' in kw:
        kw['validator'] = Function(kw['validator'])
    return SchemaNode(schema,
                      *children,
                      name=name,
                      **kw)


def mapping(name, **kw):
    return _node(Mapping(unknown='preserve'),
                 name=name, **kw)


def sequence(name, *children, **kw):
    return _node(Sequence(), name, 
                 *children, **kw)


def key(name, **kw):
    return _node(String(), name, **kw)


def chained(*validators):
    """ 
    Chain a list of predicates and raise an error on the first 
    failure. This means only the first error is shown, so it 
    makes sense to pass in predicates from the more general to 
    the more specific.
    """
    def _validator(value):
        for validator in validators:
            res = validator(value)
            if res is not True:
                return res
        return True
    return _validator


def reserved_name(terms):
    """ Check for names that have a special meaning in URLs and
    cannot be used for names. """
    terms = [t.lower() for t in terms]
    def check(name):
        if name.lower() in terms:
            return "'%s' is a reserved word and cannot be used here" % name
        return True
    return check


def name_wrap(check, name):
    """ Apply a validator to the name variable, not any of 
    the actual dimensions data. """
    def _check(value):
        return check(name)
    return _check


def in_(lst):
    """ Check that the given value is in the provided list. """
    def _check(value):
        if value not in lst:
            return "'%s' is not a valid value." % value
        return True
    return _check


def database_name(name):
    if not re.match(r"^[\w\_]+$", name):
        return ("Name must include only "
                "letters, numbers and underscores")
    return True


def nonempty_string(text):
    if not isinstance(text, basestring):
        return "Must be text, not %s" % type(text)
    if not len(text.strip()):
        return "Must have at least one non-whitespace character."
    return True




