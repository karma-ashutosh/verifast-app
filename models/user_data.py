import abc
from abc import ABC

from models.request_models import CreateUserPayload


class UserData(ABC):
    def __init__(self, username):
        self.username = username

    @abc.abstractmethod
    def render(self) -> dict:
        pass


class SimplUserData(UserData):
    def __init__(self, username, name, email):
        super().__init__(username)
        self.name = name
        self.email = email

    def render(self):
        return {
            'name': self.name,
            'email': self.email,
            'username': self.username
        }


class RSAUserData(SimplUserData):

    def __init__(self, username=None, password=None, email=None, public_key=None, private_key=None, account_id=None):
        super().__init__(username, username, email)
        self.public_key = public_key
        self.private_key = private_key
        self.account_id = account_id
        self.password = password

    def create_new_key_pair(self):
        self.public_key = "publicKey"
        self.private_key = "privateKey"
