from dataclasses import dataclass

from src.applications.events.remind import EventRemindPresenter
from src.repositories import EventRepository, EventMemberRepository
from src.models import Event, EventMember, db

@dataclass
class CreateEvenParams:
    chat_id: int
    member_id: int
    text: str
    nick_name: str
    user_name: str

class CreateEvent:
    event_repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(
        self,
        event_repository: EventRepository,
        event_member_repository: EventMemberRepository
    ):
        self.event_repository = event_repository
        self.event_member_repository = event_member_repository

    def execute(self, params: CreateEvenParams, result: EventRemindPresenter):

        event = Event(
            chat_id=params.chat_id,
            member_id=params.member_id,
            text=params.text
        )

        try:
            with db.atomic():
                self.event_repository.save(event)
                event_member = EventMember(
                    event_id=event.get_id(),
                    member_id=event.member_id,
                    nick_name=params.nick_name,
                    user_name=params.user_name
                )
                self.event_member_repository.save(event_member)

        except:
            result.error = 'Что-то пошло не так. Попробуйте позже.'

        result.event = event
        result.members = [event_member]

        pass
