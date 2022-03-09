from contract_layer.contract_client import ContractClient
from contract_layer.nft import SimpleNFT
from models.request_models import CreateNFTPayload
from models.user_data import UserData
from general_util import *


class BrownieBackedClient(ContractClient):

    def __init__(self, brand_id, user_data: UserData):
        super().__init__(brand_id, user_data)
        self.user_data: UserData = user_data
        self.username = user_data.username
        self.password = user_data.password

    def create_nft(self, payload: CreateNFTPayload) -> dict:
        nft_id = payload.nft_id
        nft_owner = self.brand_id
        nft = SimpleNFT(nft_id, nft_owner, payload.nft_attrs)
        result = brownie_create_nft(username=self.username, password=self.password, attributes=None)
        return result

    def transfer_nft(self, nft_id, to):
        brownie_transfer_nft(self.username, self.password, nft_id, to)

    def accept_transfer(self, nft_id, sender):
        brownie_claim_nft(self.username, self.password, nft_id, sender)

    def reject_transfer(self, nft_id, sender):
        brownie_reject_nft(self.username, self.password, nft_id, sender)

    def get_nft(self, nft_id) -> dict:
        return brownie_get_nft_info(nft_id)
