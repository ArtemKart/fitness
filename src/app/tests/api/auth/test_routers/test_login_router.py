from fastapi.testclient import TestClient
import pytest

from src.app.tests.utils import super_user


@pytest.mark.parametrize(
    "credentials, exp_status_code",
    [
        pytest.param(
            {
                "username": super_user.email,
                "password": super_user.password,
            },
            200,
            id="happy path",
        ),
        pytest.param(
            {
                "username": "invalid_test_username",
                "password": super_user.password,
            },
            401,
            id="invalid username",
        ),
        pytest.param(
            {
                "username": super_user.username,
                "password": "invalid_test_password",
            },
            401,
            id="invalid password",
        ),
    ],
)
def test_login_for_access_token(
    client: TestClient, credentials: dict[str, str], exp_status_code: int
) -> None:
    r = client.post("/login/token", data=credentials)
    tokens = r.json()
    assert r.status_code == exp_status_code
    if exp_status_code == 200:
        assert "access_token" in tokens
        assert tokens["access_token"]


@pytest.mark.parametrize(
    "username, exp_status_code",
    [
        pytest.param(
            super_user.email,
            200,
            id="happy path",
        ),
        pytest.param(
            "invalid_test_usename",
            404,
            id="invalid username",
        ),
    ],
)
def test_recover_password(
    client: TestClient,
    username: str,
    exp_status_code: int,
) -> None:
    r = client.post("/login/password-recovery", data={"email": username})
    assert r.status_code == exp_status_code


def test_password_reset(
    client: TestClient, test_superuser_token_headers
) -> None:
    expected_response = "Password updated successfully"
    r = client.post(
        "/login/password-reset",
        headers=test_superuser_token_headers,
        data={"new_password": "test12345"},
    )
    response = r.json()
    assert r.status_code == 200
    assert response["msg"] == expected_response
