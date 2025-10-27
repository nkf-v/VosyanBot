from abc import ABC, abstractmethod
import src.domain.events.models as models

class EventRepository(ABC):
    @abstractmethod
    def save(self, event: models.Event):
        pass

    # TODO перенести в Query
    @abstractmethod
    def getListByChatAndMember(self, chat_id: int, member_id: int):
        pass

    @abstractmethod
    def getById(self, event_id: int) -> models.Event | None:
        pass

    @abstractmethod
    def delete(self, event: models.Event):
        pass

    @abstractmethod
    def getListByIds(self, event_ids):
        pass

    @abstractmethod
    def get_list_by_chat(self, chat_id: int):
        pass


class EventMemberRepository(ABC):
    @abstractmethod
    def save(self, event_member: models.EventMember):
        pass

    @abstractmethod
    def getListByEventId(self, event_id: int):
        pass

    # TODO перенести в Query
    @abstractmethod
    def getOneByEventAndMemberId(self, event_id: int, member_id: int):
        pass

    @abstractmethod
    def delete(self, member: models.EventMember):
        pass

    @abstractmethod
    def getListByMemberId(self, member_id: int):
        pass