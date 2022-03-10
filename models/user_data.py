class UserData:

    def __init__(self, username=None, password=None, email=None, public_key=None, private_key=None, account_id=None):
        self.name = username
        self.email = email
        self.username = username
        self.password = password
        self.public_key = public_key
        self.private_key = private_key
        self.account_id = account_id

    def clear_pass(self):
        self.password = None

    def render(self) -> dict:
        return {
            'username': self.username,
            'account_id': self.account_id
        }
