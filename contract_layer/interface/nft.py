from abc import ABC, abstractmethod
from copy import copy
from datetime import datetime


class NFT(ABC):
    def __init__(self):
        self.events = []

    def publish_event(self, event: dict):
        self.events.append(event)

    @abstractmethod
    def get_attr(self, key) -> str:
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_owner(self) -> str:
        pass

    @abstractmethod
    def update_owner(self, owner_id) -> str:
        pass

    @abstractmethod
    def render(self) -> dict:
        pass


class SimpleNFT(NFT):

    def __init__(self, nft_id: str, nft_owner: str, attributes: dict):
        super().__init__()
        self.nft_id = nft_id
        self.nft_owner = nft_owner
        self.attributes = attributes
        self.publish_event({'event_type': 'created', 'timestamp': datetime.now().timestamp()})

    def get_attr(self, key) -> str:
        return self.attributes.get(key)

    def get_id(self) -> str:
        return self.nft_id

    def get_owner(self) -> str:
        return self.nft_owner

    def update_owner(self, owner_id):
        self.nft_owner = owner_id

    def render(self) -> dict:
        return {
            'id': self.nft_id,
            'owner': self.nft_owner,
            'attributes': copy(self.attributes),
            'events': copy(self.events)
        }

