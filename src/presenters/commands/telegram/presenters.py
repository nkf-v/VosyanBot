import json
from typing import List

from telegram import InlineKeyboardButton

from src.applications.events.create import EventCreatePresenter
from src.applications.events.get_list import EventListPresenter
from src.applications.events.remind import EventRemindPresenter
from src.applications.events.update import EventUpdatePresenter
from src.models import Event, EventMember


class EventListMessagePresenter(EventListPresenter):
    member_events: List[Event] = []
    invite_events: List[Event] = []
    chat_events: List[Event] = []


    def set_member_events(self, events: List[Event]) -> None:
        self.member_events = events

    def set_invite_events(self, events: List[Event]) -> None:
        self.invite_events = events

    def set_chat_events(self, events: List[Event]) -> None:
        self.chat_events = events

    def present(self) -> str:
        member_events_len = len(self.member_events)
        invite_events_len = len(self.invite_events)
        chat_events_len = len(self.chat_events)

        if (
            member_events_len == 0
            and invite_events_len == 0
            and chat_events_len == 0
        ):
            return "🤡 Чат бездельников!"

        result = []

        if member_events_len > 0:
            result.append('🎉 Твои не нужные события:')
            result = self.__add_events(self.member_events, result)

        if invite_events_len > 0:
            self.__add_div(result)

            result.append('🙌🏻 Тебя случайно добавили в эти события:')
            result = self.__add_events(self.invite_events, result)

        if chat_events_len > 0:
            self.__add_div(result)

            result.append('💬 События чата где тебя не ждут:')
            result = self.__add_events(self.chat_events, result)

        return "\n".join(result)

    def __add_events(self, events: List[Event], result: List[str]) -> List[str]:
        for event in events:
            result.append(f"ID: {event.get_id()} - {event.name}")
        return result

    def __add_div(self, result: List[str]) -> List[str]:
        if len(result) > 1:
            result.append('')
            result.append('---')
            result.append('')

        return result


class EventDetailTelegramMessagePresenter(EventCreatePresenter, EventRemindPresenter, EventUpdatePresenter):
    event: Event
    members: List[EventMember]
    error: str = None

    def set_event(self, event: Event) -> None:
        self.event = event

    def set_members(self, members: List[EventMember]) -> None:
        self.members = members

    def set_error(self, error_message: str) -> None:
        self.error = error_message

    def present(self) -> (str, List[List[InlineKeyboardButton]]):
        if self.error is not None:
            return self.error, None

        messages = [
            'Событие:',
            f"ID {self.event.get_id()} - {self.event.name}",
            self.event.text,
            'Участники:'
        ]

        for member in self.members:
            messages.append(f"- {member.user_name} (@{member.nick_name})")

        keyboard = [
            [
                InlineKeyboardButton(
                    text="Иду",
                    callback_data=json.dumps({
                        'action': 'event_invite',
                        'event_id': self.event.get_id(),
                    })
                ),
                InlineKeyboardButton(
                    text="нахрен",
                    callback_data=json.dumps({
                        'action': 'event_leave',
                        'event_id': self.event.get_id(),
                    })
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Напомнить",
                    callback_data=json.dumps({
                        'action': 'event_remind',
                        'event_id': self.event.get_id(),
                    })
                ),
                InlineKeyboardButton(
                    text="Удоли",
                    callback_data=json.dumps({
                        'action': 'event_delete',
                        'event_id': self.event.get_id(),
                    })
                ),
            ]
        ]

        return '\n'.join(messages), keyboard