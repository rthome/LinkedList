from flask import Blueprint, render_template, redirect, url_for
from flask_security import login_required, current_user

from ..entries import EntriesService
from . import route

bp = Blueprint("frontend", __name__)


@route(bp, "/")
def index():
    if current_user.is_authenticated():
        entries = EntriesService.entries_for_user(current_user)
        return render_template("index.html", entries=entries)
    else:
        return render_template("welcome.html")


@route(bp, "/about")
def about():
    return render_template("about.html")


@route(bp, "/add_entry", methods=["POST"])
@login_required
def add_entry():
    return redirect(url_for("frontend.index"))
