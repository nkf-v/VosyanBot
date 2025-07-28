import peeweedbevolve
from peewee import *
from os import getenv, path
from dotenv import load_dotenv

load_dotenv(path.abspath('.env'))

user = getenv('DB_USER')
password = getenv('DB_PASSWORD')
db_name = getenv('DB_NAME')
db_host = getenv('DB_HOST')

# Сделать фабрику и SigleTone вынести в отдельный файл
db = MySQLDatabase(
    db_name,
    user=user,
    password=password,
    host=db_host
)


class Member(Model):
    class Meta:
        database = db
        table_name = 'members'
        order_by = ('chat_id',)

    chat_id = BigIntegerField()
    member_id = BigIntegerField()
    coefficient = IntegerField()
    pidor_coefficient = IntegerField()
    full_name = CharField()
    nick_name = CharField()


class PidorStats(Model):
    class Meta:
        database = db
        order_by = ('chat_id',)

    chat_id = BigIntegerField()
    member_id = BigIntegerField()
    count = IntegerField(default=0)


class Stats(Model):
    class Meta:
        database = db
        order_by = ('chat_id',)

    chat_id = BigIntegerField()
    member_id = BigIntegerField()
    count = IntegerField(default=0)


class CurrentPidor(Model):
    class Meta:
        database = db
        order_by = ('chat_id',)

    chat_id = BigIntegerField()
    member_id = BigIntegerField()
    timestamp = BigIntegerField()


class CurrentNice(Model):
    class Meta:
        database = db
        order_by = ('chat_id',)

    chat_id = BigIntegerField()
    member_id = BigIntegerField()
    timestamp = BigIntegerField()


class CarmicDicesEnabled(Model):
    class Meta:
        database = db
        order_by = ('chat_id',)

    chat_id = BigIntegerField()

class Event(Model):
    class Meta:
        database = db
        order_by = ('chat_id',)

    chat_id = BigIntegerField()
    member_id = BigIntegerField()
    text = TextField()

class EventMember(Model):
    class Meta:
        database = db

    event_id = BigIntegerField()
    member_id = BigIntegerField()
    nick_name = CharField()
    user_name = CharField()
