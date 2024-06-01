from os import stat_result

import pytest
from constants import RESTAURANTS_URL
from fastapi import status
from httpx import AsyncClient, head

from models.restaurant_models import CreateRestaurantBody
from scripts.seed_data import SEED_RESTAURANTS
from tests.utils import successful_login


@pytest.mark.asyncio(scope="session")
async def test_successful_restaurant_creation(client: AsyncClient) -> None:
    token = await successful_login(client)

    create_restaurant_response = await client.post(
        RESTAURANTS_URL,
        json=CreateRestaurantBody(
            name="test restaurant 0",
            stars=2,
            country="Colombia",
            city="bucaramanga",
            food_type="sea",
            is_public=True,
        ).model_dump(),
        headers={"Authorization": token},
    )
    assert create_restaurant_response.status_code == status.HTTP_201_CREATED
    create_restaurant_body = create_restaurant_response.json()
    assert create_restaurant_body is not None


@pytest.mark.asyncio(scope="session")
async def test_successful_partial_update(client: AsyncClient) -> None:
    """
    Test each individual field and the full fields.
    """
    token = await successful_login(client)
    original_data = CreateRestaurantBody(
        name="test restaurant 1",
        stars=2,
        country="Colombia",
        city="bucaramanga",
        food_type="sea",
        is_public=True,
    ).model_dump()
    create_restaurant_response = await client.post(
        RESTAURANTS_URL,
        json=original_data,
        headers={"Authorization": token},
    )
    assert create_restaurant_response.status_code == status.HTTP_201_CREATED
    create_restaurant_body = create_restaurant_response.json()
    assert create_restaurant_body is not None

    new_data = {
        "name": "test restaurant 123",
        "stars": 5,
        "country": "Mexico",
        "city": "df",
        "food_type": "mexican",
    }
    restaurant_id = create_restaurant_body.get("id")
    assert restaurant_id is not None
    for key, item in new_data.items():
        update_response = await client.patch(
            RESTAURANTS_URL + restaurant_id,
            json={key: item},
            headers={"Authorization": token},
        )
        assert update_response.status_code == status.HTTP_200_OK
        update_response_body = update_response.json()
        assert update_response_body.get(key) == item

    update_full_docuemnt_response = await client.patch(
        RESTAURANTS_URL + restaurant_id,
        json=original_data,
        headers={"Authorization": token},
    )
    update_full_document_body: dict = update_full_docuemnt_response.json()
    for key, item in update_full_document_body.items():
        assert update_full_document_body.get(key) == item


@pytest.mark.asyncio(scope="session")
async def test_successful_get_public_restaurants(client: AsyncClient) -> None:
    response = await client.get(RESTAURANTS_URL + "public")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body.get("total_restaurants") >= len(SEED_RESTAURANTS)


@pytest.mark.asyncio(scope="session")
async def test_successful_create_and_get_private_restaurant(
    client: AsyncClient,
) -> None:
    token = await successful_login(client)

    create_restaurant_response = await client.post(
        RESTAURANTS_URL,
        json=CreateRestaurantBody(
            name="test restaurant 999",
            stars=2,
            country="Colombia",
            city="bucaramanga",
            food_type="sea",
            is_public=False,
        ).model_dump(),
        headers={"Authorization": token},
    )
    assert create_restaurant_response.status_code == status.HTTP_201_CREATED

    response = await client.get(
        RESTAURANTS_URL + "public", headers={"Authorization": token}
    )
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body.get("total_restaurants") >= 1
