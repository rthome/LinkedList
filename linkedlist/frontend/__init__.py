from functools import wraps

from flask import render_template

from .. import factory
from . import assets


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    assets.init_app(app)

    if not app.debug:
        for e in [404, 500]:
            app.errorhandler(e)(handle_error)

    return app


def handle_error(e):
    return render_template("errors/%s.html" % e.code), e.code


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator
