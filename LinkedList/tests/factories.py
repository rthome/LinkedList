"""
Linkedlist test factories module
"""

from datetime import datetime

from factory import Factory, Sequence, LazyAttribute
from flask_security.utils import encrypt_password

from linkedlist.core import db
from linkedlist.models import *

session = db.session

class LinkedListTestFactory(Factory):
    pass

class RoleFactory(LinkedListTestFactory):
    FACTORY_FOR = Role
    name = "admin"
    description = "Administrator"

class UserFactory(LinkedListTestFactory):
    FACTORY_FOR = User
    email = Sequence(lambda n: "user{0}@linkedlist".format(n))
    password = LazyAttribute(lambda a: encrypt_password("password"))
    last_login_at = datetime.utcnow()
    current_login_at = datetime.utcnow()
    last_login_ip = "127.0.0.1"
    current_login_ip = "127.0.0.1"
    login_count = 1
    roles = LazyAttribute(lambda a: [RoleFactory()])
    active = True

class EntryFactory(LinkedListTestFactory):
    FACTORY_FOR = Entry
    url = Sequence(lambda n: "http://www.linkedlist-test-{0}.com".format(n))
    unread = False
    added_at = datetime.utcnow()
    read_at = datetime.utcnow()
