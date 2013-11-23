import peewee

import config

_db = peewee.SqliteDatabase(config.DATABASE)

class ModelBase(peewee.Model):
	class Meta:
		database = _db

class User(ModelBase):
	email = peewee.CharField()
	password = peewee.CharField()
	join_date = peewee.DateTimeField()

class Entry(ModelBase):
    user = peewee.ForeignKeyField(User)
    url = peewee.CharField()
    title = peewee.CharField()
    unread = peewee.BooleanField()
    add_date = peewee.DateTimeField()

def connect_db():
	_db.connect()

def close_db():
	_db.close()

def create_tables():
    connect_db()
    User.create_table()
    Entry.create_table()
    close_db()
