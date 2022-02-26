import logging
from logging import Logger
from flask import Flask, request

import models.request_models
from common import setup_logging
from contract_layer.client_factory import ClientFactory
from contract_layer.interface.nft import NFT
from contract_layer.memory_contract_client import InMemoryClientProvider
from user_layer.interface.user_data_provider import InMemoryUserDataProvider
from models.request_models import CreateUserPayload
from models.user_data import UserData

app: Flask = Flask(__name__)

def get_authenticated_user_id() -> str:
    user_id = request.headers.get('userId')
    if not user_id:
        raise PermissionError("User not authenticated")
    return user_id


@app.route("/create-accout")
def create_user_account():
    payload = CreateUserPayload(request.json())
    user_data: UserData = user_data_provider.create_user(payload.username, payload)
    return user_data.render()

@app.route("/brand/<brand_id>/nft/<nft_id>")
def get_nft(brand_id, nft_id):
    caller = get_authenticated_user_id()
    client = client_factory.get_client(brand_id, caller)
    nft: dict = client.get_nft(nft_id)
    return {"response": nft}


@app.route("/brand/<brand_id>/createNFT", methods=["POST"])
def create_nft(brand_id):
    data = request.json()
    payload = models.request_models.CreateNFTPayload(data)

    caller = get_authenticated_user_id()
    client = client_factory.get_client(brand_id, caller)
    nft: dict = client.create_nft(payload)
    return {"response": nft}


@app.route("/brand/<brand_id>/nft/<nft_id>/transfer", methods=["POST"])
def approve_transfer(brand_id, nft_id):
    data = request.json()
    payload = models.request_models.TransferNFTPayload(data)

    caller = get_authenticated_user_id()
    client = client_factory.get_client(brand_id, caller)

    client.transfer_nft(nft_id, payload.receiver.user_id)
    return client.get_nft(nft_id)


@app.route("/brand/<brand_id>/nft/<nft_id>/accept-transfer", methods=["POST"])
def accept_transfer(brand_id, nft_id):

    caller = get_authenticated_user_id()
    client = client_factory.get_client(brand_id, caller)

    client.accept_transfer(nft_id)
    return client.get_nft(nft_id)


@app.route("/brand/<brand_id>/nft/<nft_id>/reject-transfer", methods=["POST"])
def reject_transfer(brand_id, nft_id):

    caller = get_authenticated_user_id()
    client = client_factory.get_client(brand_id, caller)

    client.reject_transfer(nft_id)
    return client.get_nft(nft_id)

if __name__ == "__main__":
    user_data_provider = InMemoryUserDataProvider()
    contract_client_provider = InMemoryClientProvider()
    client_factory = ClientFactory(user_data_provider, contract_client_provider)

    setup_logging()
    log: Logger = logging.getLogger("mainLogger")
