import json
from dataclasses import dataclass
from typing import List

from telegram import InlineKeyboardButton

from src.models import EventMember, Event
from src.repositories import EventRepository, EventMemberRepository

@dataclass
class EventRemindParams:
    event_id: int
    chat_id: int
    member_id: int

# TODO реализацию перенести в presenters.commands.telegram
# TODO тут оставить абстрактный класс с setters
@dataclass
class EventRemindResult:
    event: Event = None
    members: List[EventMember] = None
    error: str = None

    def present(self):
        if self.error is not None:
            return self.error, None

        messages = [
            'Событие:',
            f"- ID {self.event.get_id()} - {self.event.text}",
            '',
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
                    text="на хуй",
                    callback_data=json.dumps({
                        'action': 'event_leave',
                        'event_id': self.event.get_id(),
                    })
                ),
            ]
        ]

        return '\n'.join(messages), keyboard

class EventRemind:
    event_repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, event_repository: EventRepository, event_member_repository: EventMemberRepository):
        self.event_repository = event_repository
        self.event_member_repository = event_member_repository

    def execute(self, params: EventRemindParams, result: EventRemindResult):
        event = self.event_repository.getById(params.event_id)

        if event is None or event.chat_id != params.chat_id:
            result.error = 'Событие не найдено'
            return result

        event_members = self.event_member_repository.getListByEventId(params.event_id)
        is_event_member = False

        for member in event_members:
            if member.member_id == params.member_id:
                is_event_member = True

        if not is_event_member:
            result.error = 'Ты не участвуешь в событие. Пшол вон'
            return result

        result.event = event
        result.members = event_members

        return result
