from dataclasses import dataclass

from src.repositories import EventRepository, EventMemberRepository
from src.models import EventMember

@dataclass
class EventMemberInviteParams:
    event_id: int
    chat_id: int
    member_id: int
    nick_name: str
    user_name: str

class EventMemberInvite:
    event_repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, event_repository: EventRepository, event_member_repository: EventMemberRepository):
        self.event_repository = event_repository
        self.event_member_repository = event_member_repository

    def execute(self, params: EventMemberInviteParams):
        event = self.event_repository.getById(params.event_id)

        if event is None or event.chat_id != params.chat_id:
            return 'Событие не найдено'

        member = self.event_member_repository.getOneByEventAndMemberId(params.event_id, params.member_id)
        if member is not None:
            return 'Ты уже в событии дурачек'

        member = EventMember(
            event_id=params.event_id,
            member_id=params.member_id,
            nick_name=params.nick_name,
            user_name=params.user_name
        )

        try:
            self.event_member_repository.save(member)
        except:
            return 'Что-то пошло не так'

        return f"Ты участвуешь в событие '{event.text}'. Но лучше займись чем-нибудь полезным."
