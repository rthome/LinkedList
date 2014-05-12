from flask import Blueprint, render_template

from . import route

bp = Blueprint("frontend", __name__)

@route(bp, "/")
def index():
    return render_template("index.html")