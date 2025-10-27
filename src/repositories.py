from src.models import Member, Stats, PidorStats, CurrentNice, CurrentPidor
from peewee import DoesNotExist, Database


class MemberRepository:
    def __init__(self, db: Database):
        if db.is_closed():
            db.connect(reuse_if_open=True)

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
    def __init__(self, db: Database):
        if db.is_closed():
            db.connect(reuse_if_open=True)

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
    def __init__(self, db: Database):
        if db.is_closed():
            db.connect(reuse_if_open=True)

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
    def __init__(self, db: Database):
        if db.is_closed():
            db.connect(reuse_if_open=True)

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
    def __init__(self, db: Database):
        if db.is_closed():
            db.connect(reuse_if_open=True)

    def save(self, current: CurrentPidor):
        current.save()

    def findByChat(self, chat_id: int):
        try:
            return CurrentPidor.select().where(
                (CurrentPidor.chat_id == chat_id)
            ).get()
        except DoesNotExist:
            return None
