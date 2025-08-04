from src.repositories import EventRepository, EventMemberRepository
from src.models import db

class EventDelete:
    repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, repository: EventRepository, event_member_repository: EventMemberRepository):
        self.event_member_repository = event_member_repository
        self.repository = repository

    def execute(self, event_id: int, chat_id: int, member_id: int):
        event = self.repository.getById(event_id=event_id)

        if event is None or event.chat_id != chat_id:
            return 'Событие не найдено'

        if event.member_id != member_id:
            return "Не твое, не трожь"

        members = self.event_member_repository.getListByEventId(event_id)

        try:
            with db.atomic():
                for member in members:
                    self.event_member_repository.delete(member)

                self.repository.delete(event)
        except:
            return "Что-то пошло не так"

        return "Событие удалено"