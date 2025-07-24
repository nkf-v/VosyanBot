from src.repositories import EventRepository
from src.models import Event

class CreateEvenParams:
    chat_id: int
    member_id: int
    text: str

    def __init__(self, chat_id: int, member_id: int, text: str):
        self.chat_id = chat_id
        self.member_id = member_id
        self.text = text

class CreateEvent:
    event_repository: EventRepository

    def __init__(self, repository: EventRepository):
        self.event_repository = repository

    def execute(self, params: CreateEvenParams):
        event = Event(
            chat_id=params.chat_id,
            member_id=params.member_id,
            text=params.text
        )
        self.event_repository.save(event)

        return f"Событие сохранено.\nID: {event.get_id()}"
