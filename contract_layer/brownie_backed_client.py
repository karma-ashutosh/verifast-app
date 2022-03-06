from contract_layer.contract_client import ContractClient


class _BrownieBackedClient(ContractClient):

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

