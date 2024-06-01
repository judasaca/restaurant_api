import asyncio
import logging
import os
import sys

sys.path.append(os.getcwd())
import motor.motor_asyncio

from config import get_config
from scripts.seed_data import SEED_FIRST_USER, SEED_RESTAURANTS
from services.auth_services import create_user
from services.restaurant_services import add_restaurant


async def clear_database(
    client: motor.motor_asyncio.AsyncIOMotorClient, test_database_name: str
) -> None:

    logging.warning("Deleting database...")
    await client.drop_database(test_database_name)


async def main(
    mongo_client: motor.motor_asyncio.AsyncIOMotorClient | None = None,
    database_name: str | None = None,
) -> None:
    env = get_config()
    DATABASE_NAME = database_name or env.DATABASE_NAME

    logging.info("Cleaning database " + DATABASE_NAME)

    client: motor.motor_asyncio.AsyncIOMotorClient
    if mongo_client is None:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            env.MONGO_URL.get_secret_value()
        )
    else:
        client = mongo_client

    await clear_database(client, DATABASE_NAME)

    db_client = client.get_database(DATABASE_NAME)

    user_id = await create_user(user_data=SEED_FIRST_USER, db_client=db_client)
    for restaurant in SEED_RESTAURANTS:
        await add_restaurant(
            restaurant_info=restaurant, user_id=user_id, db_client=db_client
        )

    if env.ENVIRONMENT != "testing":
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
