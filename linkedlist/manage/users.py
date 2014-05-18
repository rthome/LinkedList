from flask_script import Command, prompt, prompt_pass
from flask_security.forms import RegisterForm
from flask_security.registerable import register_user
from werkzeug.datastructures import MultiDict

from ..services import users


class CreateUserCommand(Command):
    """Create a user"""

    def run(self):
        email = prompt("Email")
        password = prompt_pass("Password")
        password_confirm = prompt_pass("Confirm password")
        data = MultiDict(dict(email=email, password=password,
                              password_confirm=password_confirm))
        form = RegisterForm(data, csrf_enabled=False)
        if form.validate():
            user = register_user(email=email, password=password)
            print "\nUser created."
            print "<User id=%s email=%s>" % (user.id, user.email)
        else:
            print "Error:"
            for errors in form.errors.values():
                print "\n".join(errors)


class DeleteUserCommand(Command):
    """Delete a user"""

    def run(self):
        email = prompt("Email")
        user = users.first(email=email)
        if not user:
            print "Invalid user"
        else:
            users.delete(user)
            print "User deleted"


class ListUsersCommand(Command):
    """List all users"""

    def run(self):
        for u in users.all():
            print "<User id=%s email=%s>" % (u.id, u.email)
