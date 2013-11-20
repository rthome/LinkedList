import os.path, re
from flask import *

import models, config, passwords

app = Flask(__name__)
app.config.from_object(config)

def create_user(email, password):
    pass

@app.before_request
def init_base_args():
	g.base_template_args = {}
	g.base_template_args.update({"js": ["https://code.jquery.com/jquery.js", url_for("static", filename="js/bootstrap.min.js")], \
								 "css": [url_for("static", filename="css/bootstrap.min.css")]})

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        pw, pwr = request.form["password"], request.form["password_repeat"]
        error = False
        if email.strip() == "":
            flash("Please enter your email address to register!")
            error = True
        if pw != pwr:
            flash("The password you entered didn't match!")
            error = True
        if error:
            return render_template("register.html", base=g.base_template_args)
        else:
            create_user(email, pw)
            flash("Your account was created successfully!")
            return redirect(url_for("index"))
    else:
        return render_template("register.html", base=g.base_template_args)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # authenticate and log in here
        return redirect(url_for("index"))
    else:
        return render_template("login.html", base=g.base_template_args)

@app.route("/add", methods=["POST"])
def add_entry():
    if not session.get("logged_in"):
        abort(401)
    else:
        pass

@app.route("/")
def index():
    if session.get("logged_in"):
        return render_template("index.html", base=g.base_template_args)
    else:
        return redirect(url_for("login"))

def run():
	if not os.path.isfile(config.DATABASE):
		models.create_tables()
	app.run()
