from dataclasses import dataclass

from src.repositories import EventRepository, EventMemberRepository
from src.models import db

@dataclass
class EventDeleteParams:
    event_id: int
    chat_id: int
    member_id: int

class EventDelete:
    repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, repository: EventRepository, event_member_repository: EventMemberRepository):
        self.event_member_repository = event_member_repository
        self.repository = repository

    def execute(self, params: EventDeleteParams):
        event = self.repository.getById(event_id=params.event_id)

        if event is None or event.chat_id != params.chat_id:
            return 'Событие не найдено'

        if event.member_id != params.member_id:
            return 'Не твое, не трожь'

        members = self.event_member_repository.getListByEventId(params.event_id)

        try:
            with db.atomic():
                for member in members:
                    self.event_member_repository.delete(member)

                self.repository.delete(event)
        except:
            return 'Что-то пошло не так'

        return f"Вас кажется кинули. Событие {event.text} удалено"