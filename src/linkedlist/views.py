import datetime, functools

from flask import *
from flask.views import MethodView

import models, passwords

def login_required(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        if not g.get("logged_in"):
            abort(401)
        return f(*args, **kwargs)
    return decorator

class IndexView(MethodView):
    def get(self):
        if g.get("logged_in"):
            return render_template("index.html")
        else:
            return redirect(url_for("login"))

class RegistrationView(MethodView):
    def get(self):
        return render_template("register.html")

    def post(self):
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
            return render_template("register.html")
        else:
            models.User.create(email=email, password=passwords.create_hashed_password(pw), join_date=datetime.datetime.now())
            flash("Your account was created successfully!")
            return redirect(url_for("index"))

class LoginView(MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        email = request.form["email"]
        pw = request.form["password"]
        try:
            user = models.User.get(models.User.email == email)
            return redirect(url_for("index"))
        except models.User.DoesNotExist:
            return redirect(url_for("login"))

class AddView(MethodView):
    decorators = [login_required]

    def post(self):
        pass
