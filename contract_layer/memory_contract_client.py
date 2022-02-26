import json
import logging

from contract_layer.interface.contract_client_provider import ContractClientProvider
from contract_layer.interface.nft import NFT, SimpleNFT
from contract_layer.interface.contract_client import ContractClient
from models.request_models import CreateNFTPayload

ID = 'id'


class InMemoryContractProxy:
    log = logging.getLogger("InMemoryContract")

    def __init__(self, brand_id):
        self.log = InMemoryContractProxy.log
        self.brand_id = brand_id
        self._nft_storage = dict()
        self._authorization = dict()

    def create_nft(self, caller, nft: NFT):

        if self.brand_id != caller:
            raise "Only contract owner can create new NFT"

        nft_id = nft.get_id()
        if self._nft_storage.get(nft_id):
            raise ValueError("NFT with id %s already exists for brand %s".format(nft_id, self.brand_id))
        self.log.info("saving nft with Id %s, %s", nft_id, json.dumps(nft.render()))
        self._nft_storage[nft_id] = nft

    def authorize_transfer(self, caller, nft_id, to_user_id):
        if not self.__is_nft_owner(caller, nft_id):
            raise PermissionError("Only owner can authorize transfer")

        self._authorization[nft_id] = to_user_id

    def accept_transfer(self, caller, nft_id):
        authorized = self.__is_authorized_for_write(caller, nft_id)
        if authorized:
            self.__clear_authorization(nft_id)
            nft: NFT = self._nft_storage[nft_id]
            old_owner = nft.get_owner()
            nft.update_owner(caller)
            nft.publish_event({'type': 'transfer', 'from': old_owner, 'to': caller})
        else:
            raise PermissionError("Not authorized for transfer")

    def reject_transfer(self, caller, nft_id):
        authorized = self.__is_authorized_for_write(caller, nft_id)
        if authorized:
            self.__clear_authorization(nft_id)
            nft: NFT = self._nft_storage[nft_id]
            old_owner = nft.get_owner()
            nft.publish_event({'type': 'transfer_reject', 'from': old_owner, 'to': caller})
        else:
            raise PermissionError("Not authorized for transfer")

    def get_nft(self, nft_id) -> dict:
        nft: NFT = self._nft_storage[nft_id]
        if nft:
            return nft.render()
        return dict()

    def __is_nft_owner(self, nft_id, caller):
        nft: NFT = self._nft_storage.get(nft_id)
        logging.getLogger("memory").info("nft is %s", nft.render())
        return nft and nft.get_owner() is caller

    def __is_authorized_for_write(self, caller, nft_id):
        nft = self._nft_storage[nft_id]
        return nft and caller == self._authorization[nft_id]

    def __clear_authorization(self, nft_id):
        if self._authorization[nft_id]:
            self._authorization.pop(nft_id)


class _ContractFactory:
    _contract_address = dict()

    @staticmethod
    def get_contract(brand_id) -> InMemoryContractProxy:
        if not _ContractFactory._contract_address.get(brand_id):
            _ContractFactory._contract_address[brand_id] = InMemoryContractProxy(brand_id)
        return _ContractFactory._contract_address[brand_id]


class _MemoryContractClient(ContractClient):

    def __init__(self, brand_id, account_id):
        super().__init__(brand_id, account_id)
        self._contract: InMemoryContractProxy = _ContractFactory.get_contract(brand_id)

    def create_nft(self, payload: CreateNFTPayload) -> dict:
        nft_id = payload.nft_id
        nft_owner = self.brand_id
        nft = SimpleNFT(nft_id, nft_owner, payload.nft_attrs)

        self._contract.create_nft(self.account_id, nft)
        return nft.render()

    def transfer_nft(self, nft_id, to):
        self._contract.authorize_transfer(self.account_id, nft_id, to)

    def accept_transfer(self, nft_id):
        self._contract.accept_transfer(self.account_id, nft_id)

    def reject_transfer(self, nft_id):
        self._contract.reject_transfer(self.account_id, nft_id)

    def get_nft(self, nft_id) -> dict:
        return self._contract.get_nft(nft_id)

class InMemoryClientProvider(ContractClientProvider):
    def contract_client(self, brand_id, account_id) -> ContractClient:
        return _MemoryContractClient(brand_id, account_id)

