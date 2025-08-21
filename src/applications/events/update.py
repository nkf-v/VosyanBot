from dataclasses import dataclass
from typing import List

from src.models import Member, Event
from src.repositories import EventRepository, EventMemberRepository


@dataclass
class EventUpdateParams:
    chat_id: int
    member_id: int
    event_id: int
    name: str
    text: str


class EventUpdatePresenter():
    def set_event(self, event: Event) -> None:
        pass

    def set_members(self, members: List[Member]) -> None:
        pass

    def set_error(self, error: str) -> None:
        pass


class EventUpdate:
    repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, repository: EventRepository, event_member_repository: EventMemberRepository):
        self.repository = repository
        self.event_member_repository = event_member_repository

    def execute(self, params: EventUpdateParams, presenter: EventUpdatePresenter) -> None:
        event = self.repository.getById(event_id=params.event_id)

        if event is None or event.chat_id != params.chat_id:
            presenter.set_error('Событие не найдено')
            return

        if event.member_id != params.member_id:
            presenter.set_error("Не твое, не трожь")
            return

        event.name = params.name
        event.text = params.text

        try:
            self.repository.save(event)

            members = self.event_member_repository.getListByEventId(event.get_id())
        except:
            presenter.set_error('Что-то пошло не так. Пойди погуляй, траву потрогай')
            return

        presenter.set_event(event)
        presenter.set_members([member for member in members])

        return
