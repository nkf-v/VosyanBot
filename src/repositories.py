from src.models import Member, Stats, PidorStats, CurrentNice, CurrentPidor, Event
from peewee import DoesNotExist


class MemberRepository:
    def save(self, member: Member):
        member.save()

    def findByChatAndId(self, chat_id: int, member_id: int) -> Member | None:
        try:
            return Member.select().where(
                (Member.chat_id == chat_id) & (Member.member_id == member_id)
            ).get()
        except DoesNotExist:
            return None

    def delete(self, member: Member):
        member.delete_instance()


class StatsRepository:
    def save(self, stats: Stats):
        stats.save()

    def findByChatAndId(self, chat_id: int, member_id: int):
        try:
            return Stats.select().where(
                (Stats.chat_id == chat_id) & (Stats.member_id == member_id)
            ).get()
        except DoesNotExist:
            return None


class PidorStsatsRepository:
    def save(self, stats: PidorStats):
        stats.save()

    def findByChatAndId(self, chat_id: int, member_id: int):
        try:
            return PidorStats.select().where(
                (PidorStats.chat_id == chat_id) & (PidorStats.member_id == member_id)
            ).get()
        except DoesNotExist:
            return None


class CurrentNiceRepository:
    def save(self, current: CurrentNice):
        current.save()

    def findByChat(self, chat_id: int):
        try:
            return CurrentNice.select().where(
                (CurrentNice.chat_id == chat_id)
            ).get()
        except DoesNotExist:
            return None


class CurrentPidorRepository:
    def save(self, current: CurrentPidor):
        current.save()

    def findByChat(self, chat_id: int):
        try:
            return CurrentPidor.select().where(
                (CurrentPidor.chat_id == chat_id)
            ).get()
        except DoesNotExist:
            return None

class EventRepository:
    def save(self, event: Event):
        event.save()

    def getListByChatAndMember(self, chat_id: int, member_id: int):
        return Event.select().where(
            (Event.chat_id == chat_id)
        ).where(
            (Event.member_id == member_id)
        )

    def getById(self, event_id: int):
        try:
            return Event.get_by_id(event_id)
        except DoesNotExist:
            return None

    def deleteById(self, event: Event):
        event.delete()
