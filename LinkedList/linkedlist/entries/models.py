from ..core import db

class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.Integer(), db.ForeignKey("users.id"))
    url = db.Column(db.String(512))
    unread = db.Column(db.Boolean())
    added_at = db.Column(db.DateTime())
    read_at = db.Column(db.DateTime())