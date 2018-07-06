class UserBuilder:
    def __init__(self):
        self.test_user = TestUser()

    def with_name(self, name: str) -> 'UserBuilder':
        self.test_user.name = name
        return self

    def build(self) -> 'TestUser':
        return self.test_user


class TestUser:
    def __init__(self):
        self.id = '444444'
        self.name = "A tests user"
