from dataclasses import dataclass

from src.models import Event, EventMember
from src.repositories import EventRepository, EventMemberRepository

@dataclass
class EventMemberLeaveParams:
    event_id: int
    chat_id: int
    member_id: int

class EventMemberLeavePresenter:
    error: str = None
    event: Event
    member: EventMember

    def present(self) -> str:
        if self.error is not None:
            return self.error

        return f"{self.member.user_name} ({self.member.nick_name}) лох, свалил из события '{self.event.text}'. Без него будет лучше"

class EventMemberLeave:
    event_repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, event_repository: EventRepository, event_member_repository: EventMemberRepository):
        self.event_repository = event_repository
        self.event_member_repository = event_member_repository

    def execute(self, params: EventMemberLeaveParams, presenter: EventMemberLeavePresenter) -> None:
        event = self.event_repository.getById(params.event_id)

        if event is None or event.chat_id != params.chat_id:
            presenter.error = 'Событие не найдено'
            pass

        if event.member_id == params.member_id:
            presenter.error = 'Куда собрался! Ты автор события. Удаляй событие целиком раз ливаешь'
            pass

        member = self.event_member_repository.getOneByEventAndMemberId(params.event_id, params.member_id)

        if member is None:
            presenter.error = 'Зачем ливать когда тебя не приглашали?'
            pass

        try:
            self.event_member_repository.delete(member)
        except:
            presenter.error = 'Что-то пошло не так'
            pass

        presenter.event = event
        presenter.member = member
        pass