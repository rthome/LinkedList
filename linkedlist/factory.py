import os

from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from .core import db, security
from .helpers import register_blueprints
from .models import User, Role

def find_environ_config_vars():
    """
    Find environment variables containing config data and return a dict of them
    """
    # only allow secret key and database uri for now
    envvars = ["SQLALCHEMY_DATABASE_URI", "SECRET_KEY"]
    results = {}
    for key, value in os.environ.iteritems():
        if key in envvars:
            results[key] = value
    return results

def create_app(name, path, settings_override=None,
               register_security_blueprint=True):
    """Returns a Flask application object"""

    app = Flask(name, instance_relative_config=True)
    app.config.from_object("linkedlist.config") # public config
    app.config.from_pyfile("config.py", silent=True) # instance config
    app.config.from_object(settings_override) # argument override

    # patch in envvar config
    environ_config_override = find_environ_config_vars()
    for key, value in environ_config_override.iteritems():
        app.config[key] = value

    db.init_app(app)
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                      register_blueprint=register_security_blueprint)
    register_blueprints(app, name, path)

    # create database tables
    with app.app_context():
        db.create_all()

    return app
