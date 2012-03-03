from flask import Blueprint, request, redirect, url_for
from flask import render_template, flash

from grano.core import db
from grano.model import Account
from grano.validation import ValidationContext
from grano.validation import validate_account, Invalid
from grano.util import request_content, error_fill
from grano.util import invalid_dict, login_user, logout_user

section = Blueprint('account', __name__)


@section.route('/register', methods=['GET'])
def register_form():
    """ Show the sign-up form. """
    return render_template('account/register.tmpl')


@section.route('/register', methods=['POST'])
def register_save():
    """ Create an account based on the sign-up form. """
    data = request_content(request)
    context = ValidationContext()
    try:
        data = validate_account(dict(data.items()), context)
        account = Account.create(data)
        db.session.commit()
        flash("Welcome, %s!" % account.display_name, 'success')
        return redirect(url_for('home.index'))
    except Invalid as inv:
        return error_fill(register_form(),
                          data,
                          invalid_dict(inv))


@section.route('/login', methods=['GET'])
def login_form():
    """ Show the login form. """
    return render_template('account/login.tmpl')


@section.route('/login', methods=['POST'])
def login_save():
    """ Create an account based on the sign-up form. """
    data = request_content(request)
    account = Account.by_name(data.get('name'))
    if not account \
       or not account.validate_password(data.get('password')) \
       or not login_user(account):
        return error_fill(login_form(), data,
            {'name': 'Invalid username or password!'})
    flash("Welcome back, %s!" % account.display_name, 'success')
    return redirect(url_for('home.index'))


@section.route('/logout', methods=['GET'])
def logout():
    flash("You've been logged out.", 'success')
    logout_user()
    return redirect(url_for('home.index'))
