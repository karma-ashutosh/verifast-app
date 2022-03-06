from abc import ABC, abstractmethod

from models.request_models import CreateNFTPayload


class ContractClient(ABC):
    def __init__(self, brand_id, account_id):
        self.brand_id = brand_id
        self.account_id = account_id

    @abstractmethod
    def create_nft(self, payload: CreateNFTPayload) -> dict:
        pass

    @abstractmethod
    def transfer_nft(self, nft_id, to):
        pass

    @abstractmethod
    def accept_transfer(self, nft_id):
        pass

    @abstractmethod
    def reject_transfer(self, nft_id):
        pass

    @abstractmethod
    def get_nft(self, nft_id) -> dict:
        pass

