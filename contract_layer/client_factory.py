from contract_layer.contract_client import ContractClient
from models.user_data import UserData
from user_layer.user_data_provider import UserDataProvider
from contract_layer.brownie_backed_client import BrownieBackedClient


class ClientFactory:
    def __init__(self, user_data_provider: UserDataProvider):
        self.__user_data_provider = user_data_provider

    def get_client(self, brand_id, user_data: UserData) -> ContractClient:
        return BrownieBackedClient(brand_id, user_data)
