from typing import Annotated

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from dependencies.auth_dependencies import get_current_user, get_db_client
from models.auth_models import UserInDB
from models.restaurant_models import (CreateRestaurantBody, RestaurantFront,
                                      RestaurantInDB)
from services.restaurant_services import add_restaurant, find_restaurant_by_id

RestaurantRouter = APIRouter(prefix="/restaurants", tags=["Restaurant routes"])


@RestaurantRouter.post("/", response_model=RestaurantFront)
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
