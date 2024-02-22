from fastapi.testclient import TestClient
from src.app.tests.utils import test_user


def test_user_register(client: TestClient) -> None:
    data = {
        "email": test_user.email,
        "password": test_user.password,
        "username": test_user.username,
        "name": test_user.name,
    }
    r = client.post("/users", json=data)
    new_user = r.json()
    assert new_user["email"] == data["email"]
    assert new_user["name"] == data["name"]
