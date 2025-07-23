from src.repositories import EventRepository


class EventDelete:
    repository: EventRepository

    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, event_id: int, chat_id: int, member_id: int):
        event = self.repository.getById(event_id=event_id)

        if event.chat_id != chat_id or event.member_id != member_id:
            return "Не твое, не трожь"

        try:
            self.repository.deleteById(event)
        except:
            return "Что-то пошло не так. Попробуй позже"

        return "Событие удалено"