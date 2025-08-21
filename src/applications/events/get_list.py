from abc import abstractmethod, ABC
from typing import List

from src.models import Event
from src.repositories import EventRepository, EventMemberRepository


class EventListPresenter(ABC):
    @abstractmethod
    def set_member_events(self, events: List[Event]) -> None:
        pass

    @abstractmethod
    def set_invite_events(self, events: List[Event]) -> None:
        pass

    @abstractmethod
    def set_chat_events(self, events: List[Event]) -> None:
        pass


class GetEventList:
    repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, repository: EventRepository, event_member_repository: EventMemberRepository):
        self.repository = repository
        self.event_member_repository = event_member_repository

    def execute(self, chat_id: int, member_id: int, presenter: EventListPresenter):
        # Получаем события соданные участником
        member_events = self.repository.getListByChatAndMember(
            chat_id=chat_id,
            member_id=member_id
        )

        # Получаем события куда пригласили участника
        # TODO Query
        owner_event_ids = [event.id for event in member_events]

        members = self.event_member_repository.getListByMemberId(member_id)

        invite_event_ids = [member.event_id for member in members if member.event_id not in owner_event_ids]

        invite_events = self.repository.getListByIds(invite_event_ids)

        # Получаем события чата где сидит участник
        # TODO Query
        chat_events = self.repository.get_list_by_chat(chat_id)

        chat_event_ids = []
        for event in chat_events:
            if event.member_id != member_id and event.get_id() not in invite_event_ids:
                chat_event_ids.append(event.get_id())

        chat_events = self.repository.getListByIds(chat_event_ids)

        presenter.set_member_events([event for event in member_events])
        presenter.set_invite_events([event for event in invite_events])
        presenter.set_chat_events([event for event in chat_events])

        return