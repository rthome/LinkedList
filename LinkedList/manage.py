from flask_script import Manager

from linkedlist.api import create_app
from linkedlist.manage import CreateUserCommand, DeleteUserCommand, ListUsersCommand

manager = Manager(create_app())
manager.add_command("create_user", CreateUserCommand())
manager.add_command("delete_user", DeleteUserCommand())
manager.add_command("list_users", ListUsersCommand())

if __name__ == "__main__":
    manager.run()