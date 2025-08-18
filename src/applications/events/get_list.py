from typing import List

from peewee import ModelSelect

from src.repositories import EventRepository, EventMemberRepository


class EventListPresenter:
    member_events: ModelSelect
    invite_events: ModelSelect
    chat_events: ModelSelect

    def present(self) -> str:
        if (
            self.member_events.count() == 0
            and self.invite_events.count() == 0
            and self.chat_events.count() == 0
        ):
            return "🤡 Чат бездельников!"

        result = []

        if self.member_events.count() > 0:
            result.append('🎉 Твои не нужные события:')
            result = self.add_events(self.member_events, result)

        if self.invite_events.count() > 0:
            self.add_div(result)

            result.append('🙌🏻 Тебя случайно добавили в эти события:')
            result = self.add_events(self.invite_events, result)

        if self.chat_events.count() > 0:
            self.add_div(result)

            result.append('💬 События чата где тебя не ждут:')
            result = self.add_events(self.chat_events, result)

        return "\n".join(result)

    def add_events(self, events, result: List[str]) -> List[str]:
        for event in events:
            result.append(f"ID: {event.get_id()} - {event.text}")
        return result

    def add_div(self, result: List[str]) -> List[str]:
        if len(result) > 1:
            result.append('')
            result.append('---')
            result.append('')

        return result

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

        presenter.member_events = member_events
        presenter.invite_events = invite_events
        presenter.chat_events = chat_events

        pass