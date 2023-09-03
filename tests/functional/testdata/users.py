import dataclasses


@dataclasses.dataclass
class UserData:
    login: str
    password: str
    name: str


def get_users_data() -> list[UserData]:
    return [
        UserData(login="test1@test.ru", password="123qwe", name="test_user1"),
        UserData(login="test2@test.ru", password="123qwe", name="test_user2"),
        UserData(login="test3@test.ru", password="123qwe", name="test_user3"),
    ]
