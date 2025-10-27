import peewee

import src.domain.events.models as models
from src.infrastructure.events.db import DBConnectFactory
import src.domain.events.repositories as abstract_repositories

class EventRepository(abstract_repositories.EventRepository):
    __db: peewee.Database

    def __init__(self, db_connect_factory: DBConnectFactory):
        self.__db = db_connect_factory.create()

        models.Event.bind(self.__db)

    def save(self, event: models.Event):
        event.save()

    # TODO перенести в Query
    def getListByChatAndMember(self, chat_id: int, member_id: int):
        return models.Event.select().where(
            (models.Event.chat_id == chat_id)
        ).where(
            (models.Event.member_id == member_id)
        )

    def getById(self, event_id: int) -> models.Event | None:
        try:
            return models.Event.get_by_id(event_id)
        except peewee.DoesNotExist:
            return None

    def delete(self, event: models.Event):
        event.delete_instance()

    def getListByIds(self, event_ids):
        return models.Event.select().where(models.Event.id.in_(event_ids))

    def get_list_by_chat(self, chat_id: int):
        return models.Event.select().where(models.Event.chat_id == chat_id)


class EventMemberRepository(abstract_repositories.EventMemberRepository):
    __db: peewee.Database

    def __init__(self, db_connect_factory: DBConnectFactory):
        self.__db = db_connect_factory.create()

        models.EventMember.bind(self.__db)

    def save(self, event_member: models.EventMember):
        event_member.save()

    def getListByEventId(self, event_id: int):
        return models.EventMember.select().where((models.EventMember.event_id == event_id))

    # TODO перенести в Query
    def getOneByEventAndMemberId(self, event_id: int, member_id: int):
        try:
            return models.EventMember.select().where(
                (models.EventMember.event_id == event_id)
            ).where(
                (models.EventMember.member_id == member_id)
            ).get()
        except peewee.DoesNotExist:
            return None

    def delete(self, member: models.EventMember):
        member.delete_instance()

    def getListByMemberId(self, member_id: int):
        return models.EventMember.select().where(
            models.EventMember.member_id == member_id
        )
