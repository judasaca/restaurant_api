from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.restaurant_models import CreateRestaurantBody, RestaurantInDB

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
