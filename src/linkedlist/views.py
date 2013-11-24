import datetime, functools

from flask import *
from flask.views import MethodView

import models, passwords

def auth_user(user):
    session["auth"] = True
    session["user"] = dict(email=user.email, join_date=user.join_date)

def unauth_user():
    del session["user"]
    del session["auth"]

def check_auth():
    return session.get("auth", False)

def login_required(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        if check_auth():
            return f(*args, **kwargs)
        abort(401)
    return decorator

class IndexView(MethodView):
    def get(self):
        if check_auth():
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
            if passwords.check_password(pw, user.password):
                auth_user(user)
                return redirect(url_for("index"))
        except models.User.DoesNotExist:
            pass
        flash("Wrong username/password")
        return redirect(url_for("login"))

class LogoutView(MethodView):
    def get(self):
        if check_auth():
            unauth_user()
        return redirect(url_for("index"))

class AddView(MethodView):
    decorators = [login_required]

    def post(self):
        pass
