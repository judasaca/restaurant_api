from datetime import datetime

import pytest
from constants import LOGIN_URL, SIGNUP_URL
from fastapi import status
from httpx import AsyncClient

from scripts.seed_data import SEED_FIRST_USER


@pytest.mark.asyncio(scope="session")
async def test_successful_signup(client: AsyncClient) -> None:
    timestamp = datetime.now().timestamp()
    random_user_email = f"testuser{timestamp}@email.com"
    random_user_password = f"abcDEF!!{timestamp}"
    response = await client.post(
        SIGNUP_URL,
        json={"email": random_user_email, "password": random_user_password},
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio(scope="session")
async def test_fail_signup_weak_password(client: AsyncClient) -> None:
    timestamp = datetime.now().timestamp()
    random_user_email = f"testuser{timestamp}@email.com"
    passwords = ["123456789", "abcderf", "!!!!!!", "AAAAAAA", "aWsQfEm1234"]
    for password in passwords:
        response = await client.post(
            SIGNUP_URL,
            json={"email": random_user_email, "password": password},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(scope="session")
async def test_fail_signup_bad_email(client: AsyncClient) -> None:
    bad_emails = ["aaaaaaa", "12131231@", "absda@osid"]
    password = "abc123456A!"

    for email in bad_emails:
        response = await client.post(
            SIGNUP_URL,
            json={"email": email, "password": password},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio(scope="session")
async def test_successful_login(client: AsyncClient) -> None:
    response = await client.post(
        LOGIN_URL,
        json={"email": SEED_FIRST_USER.email, "password": SEED_FIRST_USER.password},
    )
    body = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert body.get("access_token") is not None


@pytest.mark.asyncio(scope="session")
async def test_fail_login_wrong_password(client: AsyncClient) -> None:
    response = await client.post(
        LOGIN_URL,
        json={"email": SEED_FIRST_USER.email, "password": "abc1243A!!!!"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio(scope="session")
async def test_fail_login_user_not_exists(client: AsyncClient) -> None:
    timestamp = datetime.now().timestamp()
    response = await client.post(
        LOGIN_URL,
        json={"email": f"aaa{timestamp}@user.com", "password": "abc1243A!!!!"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
