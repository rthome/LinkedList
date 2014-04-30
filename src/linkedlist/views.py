import datetime, functools

from flask import *
from flask.views import MethodView
from werkzeug.security import check_password_hash, generate_password_hash

from linkedlist import models, auth

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
    decorators = [auth.login_required]

    def get(self):
        return render_template("list.html", entries=models.User.get(models.User.id == session["user"]["id"]).entries())

class OpenLinkView(MethodView):
    decorators = [auth.login_required]

    def get(self, entry_id):
        user = models.User.get(models.User.id == session["user"]["id"])
        try:
            link = models.Entry.get(models.Entry.id == entry_id)
            if link.user == user:
                link.unread = False;
                link.read_date = datetime.datetime.now()
                link.save()
                return redirect(link.url)
            else:
                abort(404)
        except models.Entry.DoesNotExist:
            abort(404)
        return entry_id;

class AddView(MethodView):
    decorators = [auth.login_required]

    def post(self):
        url = request.form["url"]
        models.Entry.create(url=url, user=models.User.get(models.User.id == session["user"]["id"]))
        return redirect(url_for("list"))
