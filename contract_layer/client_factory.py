from contract_layer.interface.contract_client import ContractClient
from contract_layer.interface.contract_client_provider import ContractClientProvider
from models.user_data import UserData
from user_layer.interface.user_data_provider import UserDataProvider


class ClientFactory:
    def __init__(self, user_data_provider: UserDataProvider, contract_client_provider: ContractClientProvider):
        self.__user_data_provider = user_data_provider
        self.__contract_client_provider = contract_client_provider

    def get_client(self, brand_id, user_id) -> ContractClient:
        user_data: UserData = self.__user_data_provider.get_user_info(user_id)
        return self.__contract_client_provider.contract_client(brand_id, user_data.account_id)
