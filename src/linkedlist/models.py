from linkedlist import db, auth

import peewee

class Entry(db.Model):
    user = peewee.ForeignKeyField(auth.User)
    url = peewee.CharField()
    title = peewee.CharField(default="")
    unread = peewee.BooleanField(default=True)
    add_date = peewee.DateTimeField(default=datetime.now)
    read_date = peewee.DateTimeField(null=True)

def create_tables():
    auth.User.create_table(fail_silently=True)
    Entry.create_table(fail_silently=True)
