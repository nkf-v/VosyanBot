from src.repositories import MemberRepository


class MemberUnregister:
    repository: MemberRepository

    def __init__(self, repository: MemberRepository):
        self.repository = repository

    def execute(self, chat_id: int, member_id: int):
        member = self.repository.findByChatAndId(chat_id=chat_id, member_id=member_id)

        if member is None:
            return 'Ты и не участвовалю. Свалил.'

        try:
            self.repository.delete(member)
        except:
            return 'В этот раз тебе повезло, ты все еще в игре.'

        return f"{member.full_name}, ну и вали пидр, но мы все помним."