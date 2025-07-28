from src.repositories import EventRepository

class EventUpdateParams:
    chat_id: int
    member_id: int
    event_id: int
    text: str

    def __init__(self, chat_id: int, member_id: int, event_id: int, text: str):
        self.chat_id = chat_id
        self.member_id = member_id
        self.event_id = event_id
        self.text = text

class EventUpdate:
    repository: EventRepository

    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, params: EventUpdateParams):
        event = self.repository.getById(event_id=params.event_id)

        if event is None or event.chat_id != params.chat_id:
            return 'Событие не найдено'

        if event.member_id != params.member_id:
            return "Не твое, не трожь"

        event.text = params.text

        try:
            self.repository.save(event)
        except:
            return "Что-то пошло не так. Пойди погуляй, траву потрогай"

        return f"Событие обновлено\n- ID: {event.get_id()} - {event.text}"
