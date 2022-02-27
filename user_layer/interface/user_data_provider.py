import sqlite3
from sqlite3 import Connection, Cursor
from abc import ABC, abstractmethod

from models.request_models import CreateUserPayload
from models.user_data import UserData, SimplUserData


class UserDataProvider(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_user(self, username, payload: dict) -> UserData:
        pass

    @abstractmethod
    def get_user_info(self, username) -> UserData:
        pass


class InMemoryUserDataProvider(UserDataProvider):

    def __init__(self):
        super().__init__()
        self._user_data_storage = dict()

    def create_user(self, username, payload: CreateUserPayload) -> UserData:
        if self.__exists(username):
            raise ValueError("User with accountId %s already exists".format(username))
        self._user_data_storage[username] = SimplUserData(username=username, name=payload.username, email=payload.email)
        return self.get_user_info(username)

    def get_user_info(self, username) -> UserData:
        if not self.__exists(username):
            raise ValueError("Account not found or not authorized")
        return self._user_data_storage[username]

    def __exists(self, account_id):
        return account_id in self._user_data_storage.keys()

