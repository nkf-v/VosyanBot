from src.repositories import EventRepository, EventMemberRepository

class EventMemberLeaveParams:
    event_id: int
    chat_id: int
    member_id: int

    def __init__(self, event_id: int, chat_id: int, member_id: int):
        self.event_id = event_id
        self.chat_id = chat_id
        self.member_id = member_id

class EventMemberLeave:
    event_repository: EventRepository
    event_member_repository: EventMemberRepository

    def __init__(self, event_repository: EventRepository, event_member_repository: EventMemberRepository):
        self.event_repository = event_repository
        self.event_member_repository = event_member_repository

    def execute(self, params: EventMemberLeaveParams):
        event = self.event_repository.getById(params.event_id)

        if event is None or event.chat_id != params.chat_id:
            return 'Событие не найдено'

        if event.member_id == params.member_id:
            return 'Куда собрался! Ты автор события. Удаляй событие целиком раз ливаешь'

        member = self.event_member_repository.getOneByEventAndMemberId(params.event_id, params.member_id)

        if member is None:
            return 'Зачем ливать когда тебя не приглашали?'

        try:
            self.event_member_repository.delete(member)
        except:
            return 'Что-то пошло не так'

        return 'Ну и вали! Теперь событие пройдет куда приятнее без тебя'