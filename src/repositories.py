from src.models import Member, Stats, PidorStats, CurrentNice, CurrentPidor, Event, EventMember
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

    def getById(self, event_id: int) -> Event | None:
        try:
            return Event.get_by_id(event_id)
        except DoesNotExist:
            return None

    def delete(self, event: Event):
        event.delete_instance()

class EventMemberRepository:
    def save(self, event_member: EventMember):
        event_member.save()

    def getListByEventId(self, event_id: int):
        return EventMember.select().where((EventMember.event_id == event_id))

    def getOneByEventAndMemberId(self, event_id: int, member_id: int):
        try:
            return EventMember.select().where(
                (EventMember.event_id == event_id)
            ).where(
                (EventMember.member_id == member_id)
            ).get()
        except DoesNotExist:
            return None
