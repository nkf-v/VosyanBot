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
