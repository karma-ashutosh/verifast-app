import json
import pexpect
from datetime import datetime

network_id = "ganache-local"
contract_dir = "/home/ashutosh/work/verifast-contract"

__nft_attrs = dict()


def brownie_generate_account(username, password):
    create_account = 'brownie accounts generate {}'.format(username)
    __execute_command_and_get_console_output(create_account, password)


def brownie_get_account_address(username, password):
    operation = 'account_details'
    output_path = __file_path('account_details', username)
    get_account = "brownie run scripts/deploy_and_create {} {} {} {} --network {}".format(operation, username, password,
                                                                                          output_path, network_id)
    j = __execute_and_get(get_account, output_path)
    return j['address']


def brownie_transfer_fund(username, password, target_address, amount_eth):
    operation = 'transfer_fund'
    output_path = __file_path(operation, username)
    transfer_fund = "brownie run scripts/deploy_and_create {} {} {} {} {} {} --network {}" \
        .format(operation, username, password, target_address, amount_eth, output_path, network_id)
    j = __execute_and_get(transfer_fund, output_path)
    return j


def brownie_create_nft(username, password, attributes=None):
    operation = 'create_nft'
    output_path = __file_path(operation, username)
    create_nft = "brownie run scripts/deploy_and_create {} {} {} {} --network {}" \
        .format(operation, username, password, output_path, network_id)
    j = __execute_and_get(create_nft, output_path)
    __nft_attrs[j['tokenId']] = attributes
    return j


def brownie_transfer_nft(username, password, nft_id, target_address):
    operation = 'transfer_nft'
    output_path = __file_path(operation, username)
    transfer_nft = "brownie run scripts/deploy_and_create {} {} {} {} {} {} --network {}" \
        .format(operation, username, password, nft_id, target_address, output_path, network_id)
    j = __execute_and_get(transfer_nft, output_path)
    return j


def brownie_claim_nft(username, password, nft_id, approver):
    operation = "claim_approved"
    output_path = __file_path(operation, username)
    claim_approved = "brownie run scripts/deploy_and_create {} {} {} {} {} {} --network {}" \
        .format(operation, username, password, nft_id, approver, output_path, network_id)
    j = __execute_and_get(claim_approved, output_path)
    return j


def get_all_nft(username, password):
    operation = "get_all_nfts"
    output_path = __file_path(operation, username)
    get_all_nfts = "brownie run scripts/deploy_and_create {} {} {} {} --network {}" \
        .format(operation, username, password, output_path, network_id)
    j = __execute_and_get(get_all_nfts, output_path)
    return j


def brownie_get_nft_info(nft_id):
    operation = "get_nft"
    output_path = __file_path(operation, "NA")
    claim_approved = "brownie run scripts/deploy_and_create {} {} {} --network {}" \
        .format(operation, nft_id, output_path, network_id)
    j = __execute_and_get(claim_approved, output_path)
    return j


def brownie_reject_nft(username, password, nft_id, approver):
    raise NotImplemented()


def __file_path(operation, username):
    timestamp = int(datetime.now().timestamp() * 1000)
    output_path = '/tmp/{}_{}_{}.json'.format(timestamp, username, operation)
    return output_path


def __execute_and_get(command, output_path):
    print("running command\t {}".format(command))
    child = pexpect.spawn(command, cwd=contract_dir)
    child.wait()
    with open(output_path, 'r') as handle:
        j = json.load(handle)
    return j


def __execute_command_and_get_console_output(command: str, password) -> list:
    child = pexpect.spawn(command)
    child.expect("Enter the password to encrypt this account with:")
    child.sendline(password)
    child.wait()
    result = child.read()
    return result
