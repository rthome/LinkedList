from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_security import login_required, current_user

from ..services import entries, archive
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


@route(bp, "/archive/view")
@login_required
def view_archive():
    archived_entries = current_user.archived_entries
    return render_template("archive.html", entries=archived_entries)


@route(bp, "/archive/put/<type>")
@login_required
def do_archive(type):
    if type == "read":
        read_entries = [entry for entry in current_user.entries if not entry.unread]
        for entry in read_entries:
            archived_entry = archive.create(user_id=entry.user_id,
                                            url=entry.url,
                                            title=entry.title,
                                            added_at=entry.added_at,
                                            archived_at=datetime.utcnow())
            entries.delete(entry)
        moved_entries = len(read_entries)
        if moved_entries > 0:
            if moved_entries > 1:
                archive_message = "%d entries have been archived."
            else:
                archive_message = "%d entry has been archived."
            flash(archive_message % moved_entries, "success")
        else:
            flash("Nothing was archived.", "success")
    elif type == "byage":
        pass
    else:
        flash("No such archiving filter: %s" % type, "warning")
    return redirect(url_for("frontend.index"))


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
