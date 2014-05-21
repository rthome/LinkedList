from functools import wraps
from datetime import datetime
from urlparse import urlparse

from flask import render_template

from .. import factory
from . import assets


def urlloc(url_string):
    parsed_url = urlparse(url_string)
    return parsed_url.netloc


def timesince(instant, default="just now"):
    now = datetime.utcnow()
    diff = now - instant
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days // 30, "month", "months"),
        (diff.days // 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds // 3600, "hour", "hours"),
        (diff.seconds // 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default



def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    assets.init_app(app)

    if not app.debug:
        for e in [404, 500]:
            app.errorhandler(e)(handle_error)

    app.add_template_filter(urlloc)
    app.add_template_filter(timesince)

    return app


def handle_error(e):
    try:
        return render_template("errors/%s.html" % e.code), e.code
    except AttributeError:
        return render_template("errors/500.html"), 500


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator
