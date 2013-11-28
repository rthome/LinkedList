import datetime, functools

from flask import *
from flask.views import MethodView
from werkzeug.security import check_password_hash, generate_password_hash

import models, config

def auth_user(user):
    # update user
    user.last_login_date = datetime.datetime.now()
    user.login_count += 1
    user.save()
    # set session variables
    session["auth"] = True
    session["user"] = dict(id=user.id, email=user.email, join_date=user.join_date)

def unauth_user():
    del session["user"]
    del session["auth"]
    if "admin" in session:
        del session["admin"]

def check_auth():
    return session.get("auth", False)

def auth_admin():
    session["admin"] = True

def check_admin():
    return session.get("admin", False)

def check_admin_credentials(password):
    return check_password_hash(config.admin_pw_hash, password)

def login_required(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        if check_auth():
            return f(*args, **kwargs)
        else:
            abort(401)
    return decorator

def admin_required(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        if check_admin():
            return f(*args, **kwargs)
        else:
            abort(401)
    return decorator

class IndexView(MethodView):
    def get(self):
        if check_auth():
            return redirect(url_for("list"))
        else:
            return redirect(url_for("login"))

class RegistrationView(MethodView):
    def get(self):
        if check_auth():
            flash("You are already logged in!", "info")
            return redirect(url_for("login"))
        else:
            return render_template("register.html")

    def post(self):
        if check_auth():
            flash("You are already logged in!", "info")
            return redirect(url_for("login"))
        else:
            email = request.form["email"]
            pw = request.form["password"]
            error = False
            if email.strip() == "":
                flash("Please enter your email address to register!", "warning")
                error = True
            if len(pw) < 5:
                flash("Please enter a password that is at least 5 characters", "warning")
                error = True
            if error:
                return render_template("register.html")
            else:
                models.User.create(email=email, pwhash=generate_password_hash(pw, method="pbkdf2:sha512:1000", salt_length=8))
                flash("Your account was created successfully!", "success")
                return redirect(url_for("index"))

class LoginView(MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        if check_auth():
            return redirect(url_for("login"))
        else:
            email = request.form["email"]
            pw = request.form["password"]
            try:
                user = models.User.get(models.User.email == email)
                if check_password_hash(user.pwhash, pw):
                    auth_user(user)
                    return redirect(url_for("index"))
            except models.User.DoesNotExist:
                pass
            flash("Wrong username or password", "danger")
            return redirect(url_for("login"))

class LogoutView(MethodView):
    def get(self):
        if check_auth():
            unauth_user()
        return redirect(url_for("index"))

class ListView(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("list.html", entries=models.User.get(models.User.id == session["user"]["id"]).entries())

class OpenLinkView(MethodView):
    decorators = [login_required]

    def get(self, entry_id):
        user = models.User.get(models.User.id == session["user"]["id"])
        try:
            link = models.Entry.get(models.Entry.id == entry_id)
            if link.user == user:
                link.unread = False;
                link.save()
                return redirect(link.url)
            else:
                abort(404)
        except models.Entry.DoesNotExist:
            abort(404)
        return entry_id;

class AddView(MethodView):
    decorators = [login_required]

    def post(self):
        url = request.form["url"]
        models.Entry.create(url=url, user=models.User.get(models.User.id == session["user"]["id"]))
        return redirect(url_for("list"))

class AdminLoginView(MethodView):
    def get(self):
        if check_admin():
            return redirect(url_for("admin_panel"))
        else:
            return render_template("admin_login.html")

    def post(self):
        pw = request.form["password"]
        result = check_admin_credentials(pw)
        print(result)
        if result:
            auth_admin()
        return redirect(url_for("admin_login"))

class AdminPanelView(MethodView):
    decorators = [login_required, admin_required]

    def get(self):
        return render_template("admin_panel.html", users=models.User.select(), entries=models.Entry.select())
