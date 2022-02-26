from abc import ABC, abstractmethod

from models.request_models import CreateUserPayload
from models.user_data import UserData, SimplUserData


class UserDataProvider(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_user(self, account_id, payload: dict) -> UserData:
        pass

    @abstractmethod
    def get_user_info(self, account_id) -> UserData:
        pass


class InMemoryUserDataProvider(UserDataProvider):

    def __init__(self):
        super().__init__()
        self._user_data_storage = dict()

    def create_user(self, account_id, payload: CreateUserPayload) -> UserData:
        if self.__exists(account_id):
            raise ValueError("User with accountId %s already exists".format(account_id))
        self._user_data_storage[account_id] = SimplUserData(account_id=account_id, user_name=payload.username, user_email=payload.email)
        return self.get_user_info(account_id)

    def get_user_info(self, account_id) -> UserData:
        if not self.__exists(account_id):
            raise ValueError("Account not found or not authorized")
        return self._user_data_storage[account_id]

    def __exists(self, account_id):
        return account_id in self._user_data_storage.keys()
