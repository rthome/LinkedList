from flask import Flask
from flask_peewee.admin import Admin
from flask_peewee.auth import Auth
from flask_peewee.db import Database

from . import models

app = Flask(__name__, instance_relative_config=true)

app.config.from_object("config")
app.config.from_pyfile("config.py")

db = Database(app)
auth = Auth(app, db)
admin = Admin(app, auth)

admin.register(Auth.User)
admin.register(models.Entry)
admin.setup()
