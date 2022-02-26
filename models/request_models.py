import abc


class CreateNFTPayload:
    KEY = 'nft_data'
    ATTRS = 'attributes'
    KEY_ID = 'nft_id'

    def __init__(self, data: dict):
        nft_data = data[CreateNFTPayload.KEY]
        self.nft_id = nft_data[CreateNFTPayload.KEY_ID]
        self.nft_attrs = nft_data[CreateNFTPayload.ATTRS]


class Event(abc.ABC):
    KEY = 'event'

    def __init__(self, data: dict):
        self.event_details = data[Event.KEY]

    @abc.abstractmethod
    def json(self) -> dict:
        pass


class ReceiverInfo:
    KEY = 'receiver'

    def __init__(self, data: dict):
        receiver_info = data[ReceiverInfo.KEY]
        self.user_id = receiver_info['user_id']
        self.email = receiver_info['email']
        self.name = receiver_info['name']


class TransferNFTPayload:

    def __init__(self, data: dict):
        self.receiver = ReceiverInfo(data)

class CreateUserPayload:
    KEY = 'user_data'
    USER_NAME = 'user_name'
    NAME = 'name'
    EMAIL = 'email'

    def __init__(self, data:dict):
        user_info = data[CreateUserPayload.KEY]
        self.username = user_info[CreateUserPayload.USER_NAME]
        self.email = user_info[CreateUserPayload.EMAIL]
        self.name = user_info[CreateUserPayload.NAME]

