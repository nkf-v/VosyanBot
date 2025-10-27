from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from src.domain.events.models import EventMember, Event
from src.domain.events.repositories import EventRepository, EventMemberRepository


@dataclass
class EventRemindParams:
    event_id: int
    chat_id: int
    member_id: int


class EventRemindPresenter(ABC):
    @abstractmethod
    def set_event(self, event: Event) -> None:
        pass

    @abstractmethod
    def set_members(self, members: List[EventMember]) -> None:
        pass

    @abstractmethod
    def set_error(self, error_message: str) -> None:
        pass


class EventRemind:
    event_repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, event_repository: EventRepository, event_member_repository: EventMemberRepository):
        self.event_repository = event_repository
        self.event_member_repository = event_member_repository

    def execute(self, params: EventRemindParams, presenter: EventRemindPresenter):
        event = self.event_repository.getById(params.event_id)

        if event is None or event.chat_id != params.chat_id:
            presenter.set_error('Событие не найдено')
            return

        members = self.event_member_repository.getListByEventId(params.event_id)
        is_event_member = False

        for member in members:
            if member.member_id == params.member_id:
                is_event_member = True

        if not is_event_member:
            presenter.set_error('Ты не участвуешь в событие. Пшол вон')
            return

        presenter.set_event(event)
        presenter.set_members([member for member in members])

        return
