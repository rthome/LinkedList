import os

from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from .core import db, security
from .helpers import register_blueprints
from .models import User, Role

def create_app(name, path, settings_override=None,
               register_security_blueprint=True):
    """Returns a Flask application object"""

    app = Flask(name, instance_relative_config=True)
    app.config.from_object("linkedlist.config")
    app.config.from_pyfile("config.py", silent=True)
    app.config.from_object(settings_override)

    db.init_app(app)
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                      register_blueprint=register_security_blueprint)
    register_blueprints(app, name, path)

    return app
