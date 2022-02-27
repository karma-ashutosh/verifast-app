import datetime
import json
import logging
import sqlite3
from sqlite3 import Cursor, Connection

from models.request_models import CreateUserPayload
from models.user_data import UserData, RSAUserData
from user_layer.interface.rsa_util import generate_key_pair
from user_layer.interface.user_data_provider import UserDataProvider

from abc import abstractmethod, ABC


class AbstractSqlBackedDAO:
    def __init__(self, database, table, primary_col, row_factory=None):
        self.database = database
        self.table = table
        self.primary_col = primary_col
        self.con: Connection = sqlite3.connect('config/database/' + self.database, check_same_thread=False)

        if row_factory:
            self.con.row_factory = row_factory

        self.log = logging.getLogger('AbstractSqlBackedDAO')

        if not self.__table_exists():
            result = list(self.__create_table())
            self.log.info("Create table result %s", json.dumps(result))

    @abstractmethod
    def _create_table_command(self) -> str:
        pass

    @abstractmethod
    def _parse_create_payload(self, payload) -> dict:
        pass

    def fetch_by_primary_key(self, primary_key):
        rows = self._fetch_row(query_params={self.primary_col: primary_key})
        if len(rows) > 1:
            raise "Error!! more than one row against primary_key " + primary_key
        if len(rows) == 0:
            return None
        return rows[0]

    def insert(self, primary_key, payload):
        if self.fetch_by_primary_key(primary_key):
            raise ValueError("User with accountId {} already exists".format(primary_key))

        values = self._parse_create_payload(payload)
        self.log.info("Preapared insert row with primar key %s", primary_key)

        def consumer():
            def cur_consumer(cur: Cursor):
                columns = ', '.join(values.keys())
                placeholders = ', '.join('?' * len(values))
                sql = 'INSERT INTO {} ({}) VALUES ({})'.format(self.table, columns, placeholders)
                new_values = [int(x) if isinstance(x, bool) else x for x in values.values()]
                self.log.info("Executing %s with values %s", sql, new_values)
                return cur.execute(sql, new_values)

            return cur_consumer

        self.__wrap_in_connection(consumer())
        return self.fetch_by_primary_key(primary_key)

    def __create_table(self):
        command = self._create_table_command()
        return self.__wrap_in_connection(lambda cur: cur.execute(command))

    def __wrap_in_connection(self, connection_consumer):
        cur: Cursor = self.con.cursor()
        result = connection_consumer(cur)
        self.con.commit()
        return result

    def __table_exists(self) -> bool:
        table_name = self.table
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(table_name)
        result = list(self.__wrap_in_connection(lambda cur: cur.execute(query)))
        return len(result) > 0

    def _fetch_row(self, query_params: dict):
        query = "SELECT * FROM {} WHERE ".format(self.table)
        first = True
        for key in query_params.keys():
            value = query_params[key]
            if type(value) is not str:
                raise ValueError("Cannot query on fields other than string")

            if first:
                first = False
            else:
                query = "AND " + query

            query += "{}='{}'".format(key, value) + " "

        query += ';'

        result = list(self.__wrap_in_connection(lambda cur: cur.execute(query)))
        return result


class UserDAO(AbstractSqlBackedDAO):
    DATABASE = 'user.db'
    TABLE = 'user_table'
    PRIMARY_KEY = "username"

    def __init__(self):
        super().__init__(UserDAO.DATABASE, UserDAO.TABLE, UserDAO.PRIMARY_KEY, UserDAO._dict_factory)

    def create_user(self, username, payload: CreateUserPayload) -> UserData:
        inserted = self.insert(username, payload)
        return inserted

    def get_user_info(self, username) -> UserData:
        row = self.fetch_by_primary_key(username)
        if not row:
            raise ValueError("Account not found or not authorized")
        return row

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
        return user_info

    def _create_table_command(self) -> str:
        command = '''CREATE TABLE {} (username text, created_at real, name text, email text, public_key text, 
        private_key text, account_id text)'''.format(self.table)
        return command

    def _parse_create_payload(self, payload: CreateUserPayload):
        public_key, private_key = self.__generate_key_pair_and_register_on_blockchain()
        account_id = self.__create_blockchain_account(payload.username)

        values = {
            'username': payload.username,
            'created_at': datetime.datetime.now().timestamp(),
            'name': payload.name,
            'email': payload.email,
            'public_key': public_key,
            'private_key': private_key,
            'account_id': account_id
        }
        return values

    def __generate_key_pair_and_register_on_blockchain(self) -> (str, str):
        return generate_key_pair()

    def __create_blockchain_account(self, username) -> str:
        return username + ".eth"

