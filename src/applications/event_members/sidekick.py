from dataclasses import dataclass
from enum import Enum, member

from src.domain.events.repositories import EventRepository, EventMemberRepository
from src.domain.events.models import EventMember

class Actions(Enum):
    INC = 'inc'
    DEC = 'dec'

@dataclass
class EventMemberSideKickParams:
    event_id: int
    chat_id: int
    member_id: int
    action: Actions

class EventMemberSidekickPresenter:
    error: str = None
    member: EventMember

    def present(self) -> str:
        if self.error is not None:
            return self.error

        if self.member.sidekick_count == 0:
            return f"{self.member.user_name} ({self.member.nick_name}) будет без 🐗"

        return f"{self.member.user_name} ({self.member.nick_name}) приведет с собой {self.member.sidekick_count} 🐗"

    def is_refresh(self):
        return self.error is None


class EventMemberSidekickExecutor:
    event_repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, event_repository: EventRepository, event_member_repository: EventMemberRepository):
        self.event_repository = event_repository
        self.event_member_repository = event_member_repository

    def execute(self, params: EventMemberSideKickParams, presenter: EventMemberSidekickPresenter) -> None:
        event = self.event_repository.getById(params.event_id)

        if event is None or event.chat_id != params.chat_id:
            presenter.error = 'Событие не найдено'
            return

        member = self.event_member_repository.getOneByEventAndMemberId(params.event_id, params.member_id)
        if member is None:
            presenter.error = f"Сначала сам участвуй в событие потом докидывай своих кабанчиков"
            return

        # TODO добавить lock
        if params.action == Actions.INC:
            member.sidekick_count += 1
        elif params.action == Actions.DEC and member.sidekick_count > 0:
            member.sidekick_count -= 1

        try:
            self.event_member_repository.save(member)
        except:
            presenter.error = 'Что-то пошло не так'
            return

        presenter.member = member
