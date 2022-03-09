class UserData:

    def __init__(self, username=None, password=None, email=None, public_key=None, private_key=None, account_id=None):
        super().__init__(username, username, email)
        self.name = username
        self.email = email
        self.username = username
        self.password = password
        self.public_key = public_key
        self.private_key = private_key
        self.account_id = account_id

    def render(self) -> dict:
        pass
