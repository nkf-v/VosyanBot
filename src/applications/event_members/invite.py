from dataclasses import dataclass

from src.repositories import EventRepository, EventMemberRepository
from src.models import EventMember, Event


@dataclass
class EventMemberInviteParams:
    event_id: int
    chat_id: int
    member_id: int
    nick_name: str
    user_name: str

class EventMemberInvitePresenter:
    error: str = None
    event: Event
    member: EventMember

    def present(self) -> str:
        if self.error is not None:
            return self.error

        return f"{self.member.user_name} ({self.member.nick_name}) участвует в событие '{self.event.text}'. Но лучше бы он не соглашался"

class EventMemberInvite:
    event_repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, event_repository: EventRepository, event_member_repository: EventMemberRepository):
        self.event_repository = event_repository
        self.event_member_repository = event_member_repository

    def execute(self, params: EventMemberInviteParams, presenter: EventMemberInvitePresenter) -> None:
        event = self.event_repository.getById(params.event_id)

        if event is None or event.chat_id != params.chat_id:
            presenter.error = 'Событие не найдено'
            pass

        member = self.event_member_repository.getOneByEventAndMemberId(params.event_id, params.member_id)
        if member is not None:
            presenter.error = f"{params.user_name}, ты уже в событии {event.text}, дурачек"
            pass

        member = EventMember(
            event_id=params.event_id,
            member_id=params.member_id,
            nick_name=params.nick_name,
            user_name=params.user_name
        )

        try:
            self.event_member_repository.save(member)
        except:
            presenter.error = 'Что-то пошло не так'
            pass

        presenter.event = event
        presenter.member = member
        pass
