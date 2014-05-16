from flask_script import Manager, Command
import pep8

from linkedlist.api import create_app
from linkedlist.manage import CreateUserCommand, DeleteUserCommand, ListUsersCommand


class Pep8Command(Command):
    """Run PEP8 style checks on all LinkedList source files"""

    def run(self):
        style_guide = pep8.StyleGuide()
        style_guide.input_file("manage.py")
        style_guide.input_file("wsgi.py")
        style_guide.input_dir("linkedlist")

manager = Manager(create_app())
manager.add_command("create_user", CreateUserCommand())
manager.add_command("delete_user", DeleteUserCommand())
manager.add_command("list_users", ListUsersCommand())
manager.add_command("pep8", Pep8Command())

if __name__ == "__main__":
    manager.run()
