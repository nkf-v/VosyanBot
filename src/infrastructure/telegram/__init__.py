from dataclasses import dataclass

from src.domain import entities

@dataclass
class User(entities.User):
    nick_name: str
    user_name: str

    def get_user_name(self) -> str:
        return self.user_name

    def get_nick_name(self) -> str:
        return self.nick_name
