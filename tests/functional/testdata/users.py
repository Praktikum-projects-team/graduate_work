import dataclasses
import uuid


@dataclasses.dataclass
class UserData:
    id: str
    login: str
    password: str
    name: str


def get_users_data() -> list[UserData]:
    return [
        UserData(id=str(uuid.uuid4()), login="test1@test.ru", password="123qwe", name="test_user1"),
        UserData(id=str(uuid.uuid4()), login="test2@test.ru", password="123qwe", name="test_user2"),
        UserData(id=str(uuid.uuid4()), login="test3@test.ru", password="123qwe", name="test_user3"),
    ]
