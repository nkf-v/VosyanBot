from abc import ABC, abstractmethod


class User(ABC):
    @abstractmethod
    def get_user_name(self) -> str:
        pass

    @abstractmethod
    def get_nick_name(self) -> str:
        pass
