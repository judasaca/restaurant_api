from constants import LOGIN_URL
from fastapi import status
from httpx import AsyncClient

from scripts.seed_data import SEED_FIRST_USER


async def successful_login(client: AsyncClient) -> str:
    """
    Login using good credentials and retrieve authentication token.
    """
    response = await client.post(
        LOGIN_URL,
        json={"email": SEED_FIRST_USER.email, "password": SEED_FIRST_USER.password},
    )
    body = response.json()

    token: str = body.get("access_token")
    assert response.status_code == status.HTTP_200_OK
    assert token is not None
    return token
