from  abc import ABC, abstractmethod

from contract_layer.interface.contract_client import ContractClient


class ContractClientProvider(ABC):
    @abstractmethod
    def contract_client(self, brand_id, account_id) -> ContractClient:
        pass
