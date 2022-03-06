import json
import pexpect
from datetime import datetime

network_id = "ganache-local"
contract_dir = "/home/ashutosh/work/verifast-contract"

# def execute_command_and_get_console_output(command: str, interactive_inputs=None) -> list:
#     command = command.split(" ")
#     # stdout = str(subprocess.Popen(command, stdout=subprocess.PIPE).stdout.read())
#     execute = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
#     if interactive_inputs:
#         for inter in interactive_inputs:
#             execute.stdin.write(inter)
#     lines = execute.stdout.read().split(bytes("\\n", 'utf-8'))
#     err_lines = execute.stderr.read().split(bytes("\\n", 'utf-8'))
#     return (lines, err_lines)

def execute_command_and_get_console_output(command: str, password) -> list:
    child = pexpect.spawn(command)
    child.expect("Enter the password to encrypt this account with:")
    child.sendline(password)
    child.wait()
    result = child.read()
    return result


def brownie_get_account_address(username, password):
    operation = 'account_details'
    output_path = file_path('account_details', username)
    get_account = "brownie run scripts/deploy_and_create {} {} {} {} --network {}".format(operation, username, password, output_path, network_id)
    j = __execute_and_get(get_account, output_path)
    return j['address']


def brownie_transfer_fund(username, password, target_address, amount_eth):
    operation = 'transfer_fund'
    output_path = file_path(operation, username)
    get_account = "brownie run scripts/deploy_and_create {} {} {} {} {} {} --network {}"\
        .format(operation, username, password, target_address, amount_eth, output_path, network_id)
    j = __execute_and_get(get_account, output_path)
    return j


def file_path(operation, username):
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

