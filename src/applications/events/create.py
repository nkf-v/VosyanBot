from src.repositories import EventRepository, EventMemberRepository
from src.models import Event, EventMember

class CreateEvenParams:
    chat_id: int
    member_id: int
    text: str
    nick_name: str
    user_name: str

    def __init__(
        self,
        chat_id: int,
        member_id: int,
        text: str,
        nick_name: str,
        user_name: str
    ):
        self.chat_id = chat_id
        self.member_id = member_id
        self.text = text
        self.nick_name = nick_name
        self.user_name = user_name

class CreateEvent:
    event_repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, repository: EventRepository):
        self.event_repository = repository

    def execute(self, params: CreateEvenParams):
        event = Event(
            chat_id=params.chat_id,
            member_id=params.member_id,
            text=params.text
        )

        try:
            self.event_repository.save(event)
            self.event_member_repository.save(EventMember(
                event_id=event.get_id(),
                member_id=event.member_id,
                nick_name=params.nick_name,
                user_name=params.user_name
            ))
        except:
            return 'Что-то пошло не так. Попробуйте позже.'

        return f"Событие сохранено.\nID: {event.get_id()}"
