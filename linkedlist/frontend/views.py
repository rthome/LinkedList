from flask import Blueprint, render_template, redirect, url_for

from . import route

bp = Blueprint("frontend", __name__)


@route(bp, "/")
def index():
    return render_template("index.html")


@route(bp, "/add_entry", methods=["POST"])
def add_entry():
    return redirect(url_for("frontend.index"))
