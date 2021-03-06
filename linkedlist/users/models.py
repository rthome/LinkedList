from flask_security import UserMixin, RoleMixin

from ..core import db

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("users.id")),
    db.Column("role.id", db.Integer(), db.ForeignKey("roles.id")))


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, "name", None))

    def __ne__(self, other):
        return (self.name != other or
                self.name != getattr(other, "name", None))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(150))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime())

    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))
    entries = db.relationship("Entry", 
                              backref=db.backref("users"))
    archived_entries = db.relationship("ArchivedEntry",
                                       backref=db.backref("archivedentries"))
