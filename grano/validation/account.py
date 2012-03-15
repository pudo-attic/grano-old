from grano.model import Account
from grano.validation.util import mapping, key, chained
from grano.validation.util import nonempty_string, slug_name


def available_name(context):
    """ Check that the name is either unused or the account
    we're currently editing. """
    def _check(value):
        if context.account and context.account.name == value:
            return True
        if Account.by_name(value) is not None:
            return "This account name is already in use, please choose another."
        return True
    return _check


def confirmed_password(mapping):
    if mapping.get('password') != mapping.get('password_repeat'):
        return "The entered passwords do not match!"
    return True


def validate_account(data, context):
    schema = mapping('account', validator=chained(
        confirmed_password
        ))
    schema.add(key('name', validator=chained(
            nonempty_string,
            slug_name,
            available_name(context)
        )))
    schema.add(key('email', validator=nonempty_string))
    schema.add(key('password', validator=nonempty_string))
    schema.add(key('password_repeat', validator=nonempty_string))
    schema.add(key('fullname', missing=None))
    return schema.deserialize(data)


