from datetime import datetime

from ..core import db


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    url = db.Column(db.String(512))
    title = db.Column(db.String(512))
    unread = db.Column(db.Boolean(), default=True)
    added_at = db.Column(db.DateTime(), default=datetime.utcnow)
    read_at = db.Column(db.DateTime())


class ArchivedEntry(db.Model):
    __tablename__ = "archivedentries"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    url = db.Column(db.String(512))
    title = db.Column(db.String(512))
    added_at = db.Column(db.DateTime())
    archived_at = db.Column(db.DateTime())
