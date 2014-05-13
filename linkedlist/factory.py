import os

from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from .core import db, security
from .helpers import register_blueprints
from .models import User, Role

# Constant, previx for environment variables for linkedlist config options
LINKEDLIST_ENVVAR_PREFIX = "LINKEDLIST_CONFIG_"

def find_environ_config_vars():
    """
    Find environment variables matching LINKEDLIST_CONFIG_<name>
    and returns a dict of them
    """
    results = {}
    for key, value in os.environ.iteritems():
        if key.startswith(LINKEDLIST_ENVVAR_PREFIX):
            trimmed_key = key[len(LINKEDLIST_ENVVAR_PREFIX):]
            results[trimmed_key] = value
    return results

def create_app(name, path, settings_override=None,
               register_security_blueprint=True):
    """Returns a Flask application object"""

    environ_config_override = find_environ_config_vars()
    print environ_config_override

    app = Flask(name, instance_relative_config=True)
    app.config.from_object("linkedlist.config") # public config
    app.config.from_pyfile("config.py", silent=True) # instance config
    app.config.from_object(environ_config_override) # environment variable override
    app.config.from_object(settings_override) # argument override

    db.init_app(app)
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                      register_blueprint=register_security_blueprint)
    register_blueprints(app, name, path)

    return app
