from typing import List

from bson.objectid import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.restaurant_models import (CreateRestaurantBody, RestaurantInDB,
                                      UpdateRestaurantBody)

RESTAURANT_COLLECTION_NAME = "restaurants"


async def find_restaurant_by_id(
    id: str, db_client: AsyncIOMotorDatabase
) -> RestaurantInDB:

    restaurant_collection = db_client[RESTAURANT_COLLECTION_NAME]
    result = await restaurant_collection.find_one({"_id": ObjectId(id)})
    validated_restaurant = RestaurantInDB.model_validate(result)
    return validated_restaurant


async def add_restaurant(
    restaurant_info: CreateRestaurantBody, user_id: str, db_client: AsyncIOMotorDatabase
) -> str:
    """Insert a new restaurant in the database.
    returns: str The inserted id.
    """
    restaurant_collection = db_client[RESTAURANT_COLLECTION_NAME]
    input_data = restaurant_info.model_dump()
    input_data["created_by"] = user_id
    creation_result = await restaurant_collection.insert_one(input_data)
    return str(creation_result.inserted_id)


async def modify_restaurant(
    restaurant_info: UpdateRestaurantBody,
    restaurant_id: str,
    user_id: str,
    db_client: AsyncIOMotorDatabase,
) -> None:
    """
    Try to update restaurant info.
    Raises: HttpException 401 Unauthorized if user is trying to update a restaurant that she/he did not create.
    """
    restaurant_collection = db_client[RESTAURANT_COLLECTION_NAME]

    # Query over created by and restaurant id prevents to users updating restaurants not created by them.
    result = await restaurant_collection.update_one(
        filter={"created_by": user_id, "_id": ObjectId(restaurant_id)},
        update={
            "$set": restaurant_info.model_dump(exclude_none=True, exclude_unset=True)
        },
    )

    if result.matched_count == 0:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "User is not allowed to update this restaurant",
        )


async def find_all_public_restaurants(
    page: int, page_size: int, db_client: AsyncIOMotorDatabase
) -> List[RestaurantInDB]:
    restaurant_collection = db_client[RESTAURANT_COLLECTION_NAME]
    cursor = (
        restaurant_collection.find({"is_public": True})
        .skip(page * page_size)
        .limit(page_size)
    )
    restaurants = await cursor.to_list(page_size)
    validated_restaurants = list(
        map(lambda x: RestaurantInDB.model_validate(x), restaurants)
    )
    return validated_restaurants


async def count_all_public_restaurants(db_client: AsyncIOMotorDatabase) -> int:

    restaurant_collection = db_client[RESTAURANT_COLLECTION_NAME]
    result = await restaurant_collection.count_documents({"is_public": True})
    return result


async def find_private_restaurants(
    page: int, page_size: int, user_id: str, db_client: AsyncIOMotorDatabase
) -> List[RestaurantInDB]:
    restaurant_collection = db_client[RESTAURANT_COLLECTION_NAME]
    cursor = (
        restaurant_collection.find({"created_by": user_id, "is_public": False})
        .skip(page * page_size)
        .limit(page_size)
    )

    restaurants = await cursor.to_list(page_size)
    validated_restaurants = list(
        map(lambda x: RestaurantInDB.model_validate(x), restaurants)
    )
    return validated_restaurants


async def count_private_restaurants(
    user_id: str, db_client: AsyncIOMotorDatabase
) -> int:
    restaurant_collection = db_client[RESTAURANT_COLLECTION_NAME]
    result = await restaurant_collection.count_documents(
        {"is_public": False, "created_by": user_id}
    )
    return result
