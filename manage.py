import subprocess

from flask_script import Manager, Command
import pep8
import radon

from linkedlist.api import create_app
from linkedlist.manage import CreateUserCommand, DeleteUserCommand, ListUsersCommand


class Pep8Command(Command):
    """Run PEP8 style checks on all LinkedList source files"""

    def run(self):
        style_guide = pep8.StyleGuide()
        style_guide.input_file("manage.py")
        style_guide.input_file("wsgi.py")
        style_guide.input_dir("linkedlist")


class MetricsCommand(Command):
    """Calculate code metrics for all LinkedList source files"""

    def run(self):
        print "Calculating maintainability index"
        subprocess.call(["radon", "mi", "manage.py", "wsgi.py", "linkedlist"])
        print ""
        print "Calculating cyclomatic complexity"
        subprocess.call(["radon", "cc", "--average", "manage.py", "wsgi.py", "linkedlist"])

manager = Manager(create_app)
manager.add_command("create_user", CreateUserCommand())
manager.add_command("delete_user", DeleteUserCommand())
manager.add_command("list_users", ListUsersCommand())
manager.add_command("pep8", Pep8Command())
manager.add_command("metrics", MetricsCommand())

if __name__ == "__main__":
    manager.run()
