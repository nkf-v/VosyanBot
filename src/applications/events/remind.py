from dataclasses import dataclass

from src.repositories import EventRepository, EventMemberRepository

@dataclass
class EventRemindParams:
    event_id: int
    chat_id: int
    member_id: int

class EventRemind:
    event_repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, event_repository: EventRepository, event_member_repository: EventMemberRepository):
        self.event_repository = event_repository
        self.event_member_repository = event_member_repository

    def execute(self, params: EventRemindParams):
        event = self.event_repository.getById(params.event_id)

        if event is None or event.chat_id != params.chat_id:
            return 'Событие не найдено'

        event_members = self.event_member_repository.getListByEventId(params.event_id)
        is_event_member = False

        for member in event_members:
            if member.member_id == params.member_id:
                is_event_member = True

        if not is_event_member:
            return 'Ты не участвуешь в событие. Пшол вон'

        messages = [
            'Событие:',
            f"- ID {params.event_id} - {event.text}",
            '',
            'Участники:'
        ]

        for member in event_members:
            messages.append(f"- {member.user_name} (@{member.nick_name})")

        return '\n'.join(messages)