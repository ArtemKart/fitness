import random
import string

from fastapi.testclient import TestClient
from pydantic import BaseModel

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"

# todo: get superuser credentials from env
class SuperUser(BaseModel):
    username: str = "artem@ro.ru"
    password: str = "artem1996"


class TestUser(BaseModel):
    email: str = random_email()
    username: str = random_lower_string()
    name: str = random_lower_string()
    password: str = random_lower_string()


super_user = SuperUser()
test_user = TestUser()

def get_test_user_token_headers(client: TestClient) -> dict[str, str]:
    r = client.post(
        "/login/token",
        data={
            "username": super_user.username,
            "password": super_user.password,
        },
    )
    tokens = r.json()
    token = tokens["access_token"]
    return {"Authorization": f"Bearer {token}"}
