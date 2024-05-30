from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from models.auth_models import UserSignUp

USER_COLLECTION_NAME = "users"


async def create_user(user_data: UserSignUp, db_client: AsyncIOMotorDatabase) -> str:
    user_collection = db_client[USER_COLLECTION_NAME]
    creation_result = await user_collection.insert_one(user_data.model_dump())
    return str(creation_result.inserted_id)


async def user_exists(email: str, db_client: AsyncIOMotorDatabase) -> bool:

    user_collection = db_client[USER_COLLECTION_NAME]
    count_result = await user_collection.count_documents({"email": email})
    print(count_result)
    return count_result != 0
