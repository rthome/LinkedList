import os.path, re
from flask import *

import models, views, config

app = Flask(__name__)
app.config.from_object(config)

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
    d = {}
    # inject base css and js arguments into all templates
    d["base"] = dict(js=["https://code.jquery.com/jquery.js", url_for("static", filename="js/bootstrap.min.js")], css=[url_for("static", filename="css/bootstrap.min.css")])
    return d

# user pages
app.add_url_rule("/", view_func=views.IndexView.as_view("index"))
app.add_url_rule("/register", view_func=views.RegistrationView.as_view("register"))
app.add_url_rule("/login", view_func=views.LoginView.as_view("login"))
app.add_url_rule("/logout", view_func=views.LogoutView.as_view("logout"))
app.add_url_rule("/add", view_func=views.AddView.as_view("add"))

# admin pages
app.add_url_rule("/admin_login", view_func=views.AdminLoginView.as_view("admin_login"))
app.add_url_rule("/admin", view_func=views.AdminPanelView.as_view("admin_panel"))

def run():
	if not os.path.isfile(config.DATABASE):
		models.create_tables()
	app.run()
