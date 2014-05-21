from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_security import login_required, current_user

from ..services import entries
from ..forms import NewEntryForm
from ..models import Entry
from . import route

bp = Blueprint("frontend", __name__)


@route(bp, "/")
def index():
    if current_user.is_authenticated():
        form = NewEntryForm()
        user_entries = current_user.entries
        return render_template("index.html", entries=user_entries, new_entry_form=form)
    else:
        return render_template("welcome.html")


@route(bp, "/about")
def about():
    return render_template("about.html")


@route(bp, "/add_entry", methods=["POST"])
@login_required
def add_entry():
    form = NewEntryForm()
    if form.validate_on_submit():
        entries.create(user_id=current_user.id,
                       url=form.url.data)
    return redirect(url_for("frontend.index"))


@route(bp, "/openlink/<int:entry_id>")
@login_required
def openlink(entry_id):
    entry = entries.first(id=entry_id, user_id=current_user.id)
    if not entry:
        flash("The requested entry does not exist", "danger")
        abort(404)
    else:
        if entry.unread:
            entry.unread = False
            entry.read_at = datetime.utcnow()
            entries.save(entry)
        return redirect(entry.url)


@route(bp, "/delete/<operation>")
@login_required
def delete(operation):
    user_entries = current_user.entries
    if operation == "read":
        for entry in user_entries:
            if not entry.unread:
                entries.delete(entry)
    elif operation == "link":
        id = request.args.get("id")
        entry = entries.first(id=id, user_id=current_user.id)
        if not entry:
            flash("Entry with given id does not exist.", "danger")
        else:
            entries.delete(entry)
    elif operation == "old":
        pass
    else:
        flash("No such cleaning operation: %s" % operation, "warning")
    return redirect(url_for("frontend.index"))