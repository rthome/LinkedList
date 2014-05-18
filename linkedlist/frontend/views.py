from flask import Blueprint, render_template

from . import route

bp = Blueprint("frontend", __name__)


@route(bp, "/")
def index():
    return render_template("index.html")


@route(bp, "/add_entry")
def add_entry():
    return render_template("index.html")
