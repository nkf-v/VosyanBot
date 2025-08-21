from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from src.domain.entities import User
from src.models import Event, EventMember, db
from src.repositories import EventRepository, EventMemberRepository


@dataclass
class CreateEvenParams:
    chat_id: int
    member_id: int
    name: str
    text: str
    user: User


class EventCreatePresenter(ABC):
    @abstractmethod
    def set_event(self, event: Event) -> None:
        pass

    @abstractmethod
    def set_members(self, members: List[EventMember]) -> None:
        pass

    @abstractmethod
    def set_error(self, error_message: str) -> None:
        pass


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

    def execute(self, params: CreateEvenParams, presenter: EventCreatePresenter) -> None:
        event = Event(
            chat_id=params.chat_id,
            member_id=params.member_id,
            name=params.name,
            text=params.text
        )

        try:
            with db.atomic():
                self.event_repository.save(event)
                event_member = EventMember(
                    event_id=event.get_id(),
                    member_id=event.member_id,
                    nick_name=params.user.get_nick_name(),
                    user_name=params.user.get_user_name()
                )
                self.event_member_repository.save(event_member)

        except:
            presenter.set_error('Что-то пошло не так. Попробуйте позже.')
            return

        presenter.set_event(event)
        presenter.set_members([event_member])

        return
