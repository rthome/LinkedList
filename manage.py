from flask_script import Manager, Command

from linkedlist.api import create_app
from linkedlist.manage import CreateUserCommand, DeleteUserCommand, ListUsersCommand


class Pep8Command(Command):
    """Run PEP8 style checks on all LinkedList source files"""

    def run(self):
        import pep8
        style_guide = pep8.StyleGuide()
        style_guide.input_file("manage.py")
        style_guide.input_file("wsgi.py")
        style_guide.input_dir("linkedlist")


class MetricsCommand(Command):
    """Calculate code metrics for all LinkedList source files"""

    def run(self):
        import subprocess
        print "Calculating maintainability index"
        subprocess.call(["radon", "mi", "manage.py", "wsgi.py", "linkedlist"])
        print ""
        print "Calculating cyclomatic complexity"
        subprocess.call(["radon", "cc", "--average", "manage.py", "wsgi.py", "linkedlist"])


class PycleanCommand(Command):
    """Delete .pyc files in the linkedlist source tree"""

    def run(self):
        import os
        counter = 0
        for dirpath, dirnames, filenames in os.walk("linkedlist"):
            for file in filenames:
                if file.endswith(".pyc"):
                    fullpath = os.path.join(dirpath, file)
                    os.remove(fullpath)
                    counter += 1
                    print "Deleted %s" % fullpath
        print "------------------------------"
        print "Deleted %d pyc files" % counter
        print ""

manager = Manager(create_app)
manager.add_command("create", CreateUserCommand, namespace="users")
manager.add_command("delete", DeleteUserCommand, namespace="users")
manager.add_command("list", ListUsersCommand, namespace="users")
manager.add_command("pep8", Pep8Command)
manager.add_command("metrics", MetricsCommand)
manager.add_command("pyc", PycleanCommand)

if __name__ == "__main__":
    manager.run()
