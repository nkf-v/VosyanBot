from src.repositories import EventRepository


class GetEventList:
    repository: EventRepository

    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, chat_id: int, member_id: int):
        event_list = self.repository.getListByChatAndMember(
            chat_id=chat_id,
            member_id=member_id
        )

        if event_list.count() == 0:
            return ["Ты бездельник!"]

        result = ["Ваш список дел:"]
        for event in event_list:
            result.append(f"- ID: {event.get_id()} - {event.text}")

        return result
