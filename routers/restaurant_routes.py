import math
from typing import Annotated

from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from dependencies.auth_dependencies import get_current_user, get_db_client
from models.auth_models import UserInDB
from models.restaurant_models import (CreateRestaurantBody,
                                      GetRestaurantsResponse, RestaurantFront,
                                      RestaurantInDB, UpdateRestaurantBody)
from services.restaurant_services import (add_restaurant,
                                          count_all_public_restaurants,
                                          count_private_restaurants,
                                          find_all_public_restaurants,
                                          find_private_restaurants,
                                          find_restaurant_by_id,
                                          modify_restaurant)

RestaurantRouter = APIRouter(prefix="/restaurants", tags=["Restaurant routes"])


@RestaurantRouter.post(
    "/", response_model=RestaurantFront, status_code=status.HTTP_201_CREATED
)
async def create_new_restaurant(
    restaurant_info: CreateRestaurantBody,
    current_user: Annotated[UserInDB, Depends(get_current_user)],
    db_client: Annotated[AsyncIOMotorDatabase, Depends(get_db_client)],
) -> RestaurantFront:
    inserted_id = await add_restaurant(
        restaurant_info=restaurant_info, user_id=current_user.id, db_client=db_client
    )
    created_restaurant = await find_restaurant_by_id(inserted_id, db_client)
    return RestaurantFront.model_validate(created_restaurant.model_dump())


@RestaurantRouter.patch(
    "/{restaurant_id}",
    response_model=RestaurantFront,
    description="Partial update of restaurant by id. All fields in the body are optionals.",
    status_code=status.HTTP_200_OK,
)
async def update_restaurant(
    restaurant_info: UpdateRestaurantBody,
    restaurant_id: str,
    current_user: Annotated[UserInDB, Depends(get_current_user)],
    db_client: Annotated[AsyncIOMotorDatabase, Depends(get_db_client)],
) -> RestaurantFront:
    if not ObjectId.is_valid(restaurant_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Restaurant id must be a valid mongodb id string",
        )
    await modify_restaurant(
        restaurant_info=restaurant_info,
        restaurant_id=restaurant_id,
        user_id=current_user.id,
        db_client=db_client,
    )
    updated_restaurant = await find_restaurant_by_id(restaurant_id, db_client)
    return RestaurantFront.model_validate(updated_restaurant.model_dump())


@RestaurantRouter.get(
    "/public",
    response_model=GetRestaurantsResponse,
    description="Get all the public restaurants created by any user. You do not need to be authenticated.",
)
async def get_all_public_restaurants(
    db_client: Annotated[AsyncIOMotorDatabase, Depends(get_db_client)],
    page: int = Query(0, description="Starts at 0", ge=0),
    page_size: int = Query(10, description="Default page size = 10", ge=1),
) -> dict:
    restaurants = await find_all_public_restaurants(
        page=page, page_size=page_size, db_client=db_client
    )
    total_restaurants = await count_all_public_restaurants(db_client)
    return {
        "restaurants": restaurants,
        "current_page": page,
        "page_size": page_size,
        "total_restaurants": total_restaurants,
        "available_pages": math.floor(total_restaurants / page_size) + 1,
    }


@RestaurantRouter.get(
    "/private",
    response_model=GetRestaurantsResponse,
    description="Get the private restaurants that you created. You need to be authenticated.",
)
async def get_all_private_restaurants(
    db_client: Annotated[AsyncIOMotorDatabase, Depends(get_db_client)],
    current_user: Annotated[UserInDB, Depends(get_current_user)],
    page: int = Query(0, description="Starts at 0", ge=0),
    page_size: int = Query(10, description="Default page size = 10", ge=1),
) -> dict:
    restaurants = await find_private_restaurants(
        page=page, page_size=page_size, user_id=current_user.id, db_client=db_client
    )
    total_restaurants = await count_private_restaurants(
        user_id=current_user.id, db_client=db_client
    )
    return {
        "restaurants": restaurants,
        "current_page": page,
        "page_size": page_size,
        "total_restaurants": total_restaurants,
        "available_pages": math.floor(total_restaurants / page_size) + 1,
    }
