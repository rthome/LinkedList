import os.path, urllib.parse
from datetime import datetime
from flask import *

from linkedlist import models, views, config

JS_FILES = [("https://code.jquery.com/jquery.js", False), ("js/bootstrap.min.js", True), ("js/list.min.js", True)]
CSS_FILES = [("css/bootstrap.min.css", True), ("css/bootstrap.min.css", True), ("css/bootstrap-theme.min.css", True), ("css/style.css", True)]

app = Flask(__name__)
app.config.from_object(config)

@app.template_filter()
def urlloc(s):
    o = urllib.parse.urlparse(s)
    return o.netloc

@app.template_filter()
def timesince(dt, default="just now"):
    now = datetime.now()
    diff = now - dt
    periods = (
        (diff.days // 365, "year", "years"),
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

# open db connection on every request, close on every response
@app.before_request
def db_before_request():
    models.connect_db()

@app.after_request
def db_after_request(response):
    models.close_db()
    return response

@app.context_processor
def inject_base_args():
    def process_file_list(lst):
        results = []
        for path, p in lst:
            full_path = None
            if p:
                full_path = url_for("static", filename=path)
            else:
                full_path = path
            if config.DEBUG:
                if full_path.rfind(".min.js") > 0:
                    full_path = full_path.replace(".min.js", ".js")
            results.append(full_path)
        return results
    js = process_file_list(JS_FILES)
    css = process_file_list(CSS_FILES)
    return dict(base=dict(js=js, css=css))

# user pages
app.add_url_rule("/", view_func=views.IndexView.as_view("index"))
app.add_url_rule("/list", view_func=views.ListView.as_view("list"))
app.add_url_rule("/list/add", view_func=views.AddView.as_view("add_entry"))
app.add_url_rule("/list/go/<int:entry_id>", view_func=views.OpenLinkView.as_view("openlink"))

# registration & login
app.add_url_rule("/register", view_func=views.RegistrationView.as_view("register"))
app.add_url_rule("/login", view_func=views.LoginView.as_view("login"))
app.add_url_rule("/logout", view_func=views.LogoutView.as_view("logout"))

# admin pages
app.add_url_rule("/admin/login", view_func=views.AdminLoginView.as_view("admin_login"))
app.add_url_rule("/admin", view_func=views.AdminPanelView.as_view("admin_panel"))

def run():
    if not os.path.isfile(config.DATABASE):
        models.create_tables()
    app.run()
