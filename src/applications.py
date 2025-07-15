from db_functions import create_user
from models import Member, Stats, PidorStats, CurrentNice, CurrentPidor
from repositories import (
    MemberRepository,
    StatsRepository,
    PidorStsatsRepository,
    CurrentNiceRepository,
    CurrentPidorRepository
)

class MemberRegistrationDto:
    chat_id: int
    member_id: int
    user_full_name: int
    user_nickname: int

    def __init__(self, chat_id, member_id, user_full_name, user_nickname):
        self.chat_id = chat_id
        self.member_id = member_id
        self.user_full_name = user_full_name
        self.user_nickname = user_nickname
        pass

class MemberRegistration:
    member_repository: MemberRepository
    stats_repository: StatsRepository
    pidor_stats_repository: PidorStsatsRepository
    current_nice_repository: CurrentNiceRepository
    current_pidor_repository: CurrentPidorRepository

    def __init__(
            self,
            member_repository: MemberRepository,
            stats_repository: StatsRepository,
            pidor_stats_repository: PidorStsatsRepository,
            current_nice_repository: CurrentNiceRepository,
            current_pidor_repository: CurrentPidorRepository,
        ):
        self.member_repository = member_repository
        self.stats_repository = stats_repository
        self.pidor_stats_repository = pidor_stats_repository
        self.current_nice_repository = current_nice_repository
        self.current_pidor_repository = current_pidor_repository
        pass

    def execute(self, params: MemberRegistrationDto):
        member = self.member_repository.findByChatAndId(chat_id=params.chat_id, member_id=params.member_id)

        if member is not None:
            # Выделить формирование текста 
            return f"{params.user_full_name}, ты дурачек? Зачем ты регаешься ещё раз?"

        member = Member(
            chat_id=params.chat_id,
            member_id=params.member_id,
            coefficient=10,
            pidor_coefficient=10,
            full_name=params.user_full_name,
            nick_name=params.user_nickname,
        )

        self.member_repository.save(member)

        stats = self.stats_repository.findByChatAndId(
            chat_id=params.chat_id,
            member_id=params.member_id
        )
        if stats is None:
            stats = Stats(
                chat_id=params.chat_id,
                member_id=params.member_id,
                count=0
            )
            self.stats_repository.save(stats)

        pidorStats = self.pidor_stats_repository.findByChatAndId(
            chat_id=params.chat_id,
            member_id=params.member_id
        )
        if pidorStats is None:
            pidorStats = PidorStats(
                chat_id=params.chat_id,
                member_id=params.member_id,
                count=0
            )
            self.pidor_stats_repository.save(pidorStats)

        # Вынести в отдельную логику
        currentNice = self.current_nice_repository.findByChat(params.chat_id)
        if currentNice is None:
            currentNice = CurrentNice(chat_id=params.chat_id, member_id=0, timestamp=0)
            self.current_nice_repository.save(currentNice)

        # Вынести в отдельную логику
        currentPidor = self.current_pidor_repository.findByChat(params.chat_id)
        if currentPidor is None:
            currentPidor = CurrentPidor(chat_id=params.chat_id, member_id=0, timestamp=0)
            self.current_pidor_repository.save(currentPidor)

        return f"{params.user_full_name}, хана тебе"