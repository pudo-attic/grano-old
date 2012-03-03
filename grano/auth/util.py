from grano.core import current_user


def logged_in():
    return not current_user.is_anonymous()
