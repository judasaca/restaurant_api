import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List

import httpx
import motor.motor_asyncio
from fastapi import FastAPI, HTTPException, requests, status

from config import get_config
from models.common_models import RandomNumberResponse
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


@app.get(
    "/random_number",
    tags=["Extra endpoints"],
    description="This endpoint makes a get request to http://www.randomnumberapi.com/api/v1.0/random and retrieve a random number between 0 and 100",
    response_model=RandomNumberResponse,
)
async def extract_random_number() -> dict:
    api_url = "http://www.randomnumberapi.com/api/v1.0/random"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            number_list: List[int] = response.json()
            if len(number_list) > 0:
                return {"random_number": number_list[0]}
            else:
                raise Exception("Empty body response from external api")
        except Exception as e:
            logging.error(str(e))
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "Imposible to retrive the random number",
            )


app.include_router(AuthRouter)
app.include_router(RestaurantRouter)
