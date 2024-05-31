from contextlib import asynccontextmanager
from typing import AsyncGenerator

import motor.motor_asyncio
from fastapi import FastAPI

from config import get_config
from routers.auth_router import AuthRouter
from routers.restaurant_routes import RestaurantRouter


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator:
    # App start
    env = get_config()
    client = motor.motor_asyncio.AsyncIOMotorClient(env.MONGO_URL.get_secret_value())
    app_instance.state.db_client = client.get_database(env.DATABASE_NAME)
    yield
    client.close()

    # app ends


app = FastAPI(lifespan=lifespan)


app.include_router(AuthRouter)
app.include_router(RestaurantRouter)
