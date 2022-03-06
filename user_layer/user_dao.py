import datetime
import json

from commons.dao import AbstractSqlBackedDAO
from commons.rsa_util import generate_key_pair
from models.request_models import CreateUserPayload
from models.user_data import RSAUserData, UserData
from general_util import execute_command_and_get_console_output, brownie_get_account_address, brownie_transfer_fund


class UserDAO(AbstractSqlBackedDAO):
    DATABASE = 'user.db'
    TABLE = 'user_table'
    PRIMARY_KEY = "username"

    def __init__(self):
        super().__init__(UserDAO.DATABASE, UserDAO.TABLE, UserDAO.PRIMARY_KEY, UserDAO._dict_factory)

    @staticmethod
    def _dict_factory(cursor, row) -> UserData:
        user_info = RSAUserData()
        for idx, col in enumerate(cursor.description):
            value = row[idx]
            col_name = col[0]
            if col_name == 'username':
                user_info.username = value
            elif col_name == 'name':
                user_info.name = value
            elif col_name == 'email':
                user_info.email = value
            elif col_name == 'public_key':
                user_info.public_key = value
            elif col_name == 'private_key':
                user_info.private_key = value
            elif col_name == 'account_id':
                user_info.account_id = value
            elif col_name == 'password':
                user_info.password = value
        return user_info

    def _create_table_command(self) -> str:
        command = '''CREATE TABLE {} (username text, created_at real, name text, email text, public_key text, 
        private_key text, account_id text, password text)'''.format(self.table)
        return command

    def _parse_create_payload(self, payload: CreateUserPayload):
        public_key, private_key = self.__generate_key_pair_and_register_on_blockchain()
        account_id = self.__create_blockchain_account(payload.username, payload.password, private_key)

        values = {
            'username': payload.username,
            'created_at': datetime.datetime.now().timestamp(),
            'name': payload.name,
            'email': payload.email,
            'public_key': public_key,
            'private_key': private_key,
            'account_id': account_id,
            'password': payload.password
        }
        return values

    def __generate_key_pair_and_register_on_blockchain(self) -> (str, str):
        return generate_key_pair()

    def __create_blockchain_account(self, username, password, private_key) -> str:
        create_account = 'brownie accounts generate {}'.format(username)
        result = execute_command_and_get_console_output(create_account, password)
        account_address = brownie_get_account_address(username, password)
        transfer_fund = brownie_transfer_fund('ashutosh', 'lambda', account_address, 5)
        print("Transferred fund to new account: {}".format(json.dumps(transfer_fund)))
        return username

