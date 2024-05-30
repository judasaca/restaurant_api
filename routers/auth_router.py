from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestErrorModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import ValidationError

from dependencies.auth_dependencies import get_db_client
from models.auth_models import UserSignUp
from services.auth_services import create_user, user_exists

AuthRouter = APIRouter(prefix="/auth", tags=["Auth routes"])


@AuthRouter.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    user_data: UserSignUp, db_client: AsyncIOMotorDatabase = Depends(get_db_client)
) -> None:

    if await user_exists(user_data.email, db_client):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "User already exists in database"
        )

    result = await create_user(user_data, db_client)
    if not result:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "User not created")
