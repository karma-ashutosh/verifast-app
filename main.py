import json
import logging
from logging import Logger
from flask import Flask, request, url_for

import models.request_models
from common import setup_logging
from contract_layer.client_factory import ClientFactory
from contract_layer.interface.nft import NFT
from contract_layer.memory_contract_client import InMemoryClientProvider
from user_layer.interface.sql_lite_backed_provider import UserDAO
from user_layer.interface.user_data_provider import InMemoryUserDataProvider
from models.request_models import CreateUserPayload
from models.user_data import UserData

app: Flask = Flask(__name__)
# user_data_provider = InMemoryUserDataProvider()
user_data_provider = UserDAO()
contract_client_provider = InMemoryClientProvider()
client_factory = ClientFactory(user_data_provider, contract_client_provider)

setup_logging()
log: Logger = logging.getLogger("mainLogger")


def get_authenticated_user_id() -> str:
    user_id = request.headers.get('user-id')
    if not user_id:
        raise PermissionError("User not authenticated")
    return user_id


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map", methods=["GET"])
def site_map():
    links = {}
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "POST" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links[url] = rule.endpoint
            log.info("Setting %s for %s", url, rule.endpoint)
    return links
    # links is now a list of url, endpoint tuples


@app.route("/new-account", methods=["POST"])
def create_user_account():
    payload = CreateUserPayload(request.json)
    user_data: UserData = user_data_provider.insert(payload.username, payload)
    return user_data.render()


@app.route("/brand/<brand_id>/nft/<nft_id>", methods=["GET"])
def get_nft(brand_id, nft_id):
    caller = get_authenticated_user_id()
    client = client_factory.get_client(brand_id, caller)
    nft: dict = client.get_nft(nft_id)
    return {"response": nft}


@app.route("/brand/<brand_id>/create-nft", methods=["POST"])
def create_nft(brand_id):
    data = request.json
    payload = models.request_models.CreateNFTPayload(data)

    caller = get_authenticated_user_id()
    client = client_factory.get_client(brand_id, caller)
    nft: dict = client.create_nft(payload)
    return json.dumps({"response": nft}, indent=1)


@app.route("/brand/<brand_id>/nft/<nft_id>/transfer", methods=["POST"])
def approve_transfer(brand_id, nft_id):
    data = request.json
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
