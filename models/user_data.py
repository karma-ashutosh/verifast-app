import abc
from abc import ABC

from models.request_models import CreateUserPayload


class UserData(ABC):
    def __init__(self, account_id):
        self.account_id = account_id

    @abc.abstractmethod
    def render(self) -> dict:
        pass


class SimplUserData(UserData):
    def __init__(self, account_id, user_name, user_email):
        super().__init__(account_id)
        self.user_name = user_name
        self.email = user_email

    def render(self):
        return {
            'user_name': self.user_name,
            'email': self.email,
            'account_id': self.account_id
        }


class RSAUserData(SimplUserData):

    def __init__(self, account_id, user_name, user_email, public_key=None, private_key=None):
        super().__init__(account_id, user_name, user_email)
        self.public_key = public_key
        self.private_key = private_key

    def create_new_key_pair(self):
        self.public_key = "publicKey"
        self.private_key = "privateKey"
