from abc import ABC, abstractmethod

from models.request_models import CreateNFTPayload
from models.user_data import UserData


class ContractClient(ABC):
    def __init__(self, brand_id, user_data: UserData):
        self.brand_id = brand_id
        self.user_data = user_data

    @abstractmethod
    def create_nft(self, payload: CreateNFTPayload) -> dict:
        pass

    @abstractmethod
    def transfer_nft(self, nft_id, to):
        pass

    @abstractmethod
    def accept_transfer(self, nft_id, sender):
        pass

    @abstractmethod
    def reject_transfer(self, nft_id, sender):
        pass

    @abstractmethod
    def get_nft(self, nft_id) -> dict:
        pass

