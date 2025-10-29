import peeweedbevolve
import peewee

class Event(peewee.Model):
    class Meta:
        order_by = ('chat_id',)

    chat_id = peewee.BigIntegerField()
    member_id = peewee.BigIntegerField()
    name = peewee.TextField(default='')
    text = peewee.TextField()

class EventMember(peewee.Model):
    event_id = peewee.BigIntegerField()
    member_id = peewee.BigIntegerField()
    nick_name = peewee.CharField()
    user_name = peewee.CharField()
    sidekick_count = peewee.SmallIntegerField(default=0)


# Заглушки

class Member(peewee.Model):
    class Meta:
        table_name = 'members'
        evolve = False


class PidorStats(peewee.Model):
    class Meta:
        evolve = False


class Stats(peewee.Model):
    class Meta:
        evolve = False


class CurrentPidor(peewee.Model):
    class Meta:
        evolve = False


class CurrentNice(peewee.Model):
    class Meta:
        evolve = False


class CarmicDicesEnabled(peewee.Model):
    class Meta:
        evolve = False