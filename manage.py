from flask_script import Manager, Command
import pep8

from linkedlist.api import create_app
from linkedlist.manage import CreateUserCommand, DeleteUserCommand, ListUsersCommand

class Pep8Command(Command):

    def run(self):
        style_guide = pep8.StyleGuide()
        style_guide.input_dir(".")

manager = Manager(create_app())
manager.add_command("create_user", CreateUserCommand())
manager.add_command("delete_user", DeleteUserCommand())
manager.add_command("list_users", ListUsersCommand())
manager.add_command("pep8", Pep8Command())

if __name__ == "__main__":
    manager.run()
