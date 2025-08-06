from src.repositories import EventRepository, EventMemberRepository


class GetEventList:
    repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, repository: EventRepository, event_member_repository: EventMemberRepository):
        self.repository = repository
        self.event_member_repository = event_member_repository

    def execute(self, chat_id: int, member_id: int):
        event_list = self.repository.getListByChatAndMember(
            chat_id=chat_id,
            member_id=member_id
        )

        result = ["🤡 Ты бездельник!"]

        if event_list.count() != 0:
            result = ['🎉 Твои ни никому не нужные события:']
            for event in event_list:
                result.append(f"ID: {event.get_id()} - {event.text}")

        owner_event_ids = [event.id for event in event_list]

        members = self.event_member_repository.getListByMemberId(member_id)

        event_ids = [member.event_id for member in members if member.event_id not in owner_event_ids]

        member_events = self.repository.getListByIds(event_ids)

        if member_events.count() == 0:
            return result

        if len(result) > 1:
            result.append('')
            result.append('---')
            result.append('')

        result.append('🙌🏻 События где тебя не ждут:')

        for event in member_events:
            if event.member_id != member_id:
                result.append(f"ID: {event.get_id()} - {event.text}")

        return result
