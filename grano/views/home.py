from flask import Blueprint, request, redirect, url_for
from flask import render_template

section = Blueprint('home', __name__)

@section.route('/')
def index():
    return render_template('index.tmpl')


