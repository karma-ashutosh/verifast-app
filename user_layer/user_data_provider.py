from abc import ABC, abstractmethod

from models.request_models import CreateUserPayload
from models.user_data import UserData
from user_layer.user_dao import UserDAO


class UserDataProvider(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_user(self, username, payload: CreateUserPayload) -> UserData:
        pass

    @abstractmethod
    def get_user_info(self, username) -> UserData:
        pass


class DaoBackedUserDataProvider(UserDataProvider):
    def __init__(self, user_dao: UserDAO):
        super().__init__()
        self.user_dao: UserDAO = user_dao

    def create_user(self, username, payload: CreateUserPayload) -> UserData:
        return self.user_dao.insert(username, payload)

    def get_user_info(self, username) -> UserData:
        row = self.user_dao.fetch_by_primary_key(username)
        if not row:
            raise ValueError("Account not found or not authorized")
        return row

