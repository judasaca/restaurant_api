from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from dependencies.auth_dependencies import (authorization_header,
                                            get_current_user, get_db_client)
from exceptions.auth_exceptions import InvalidLoginCredentialsException
from models.auth_models import Token, UserInDB, UserLogin, UserSignUp
from services.auth_services import create_user, find_user_by_email, user_exists
from utils.security_utils import create_access_token, password_is_correct

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


@AuthRouter.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_data: UserLogin, db_client: AsyncIOMotorDatabase = Depends(get_db_client)
) -> Token:
    user = await find_user_by_email(email=user_data.email, db_client=db_client)
    if user is None:
        raise InvalidLoginCredentialsException
    if not password_is_correct(
        password=user_data.password, real_hashed_password=user.password
    ):
        raise InvalidLoginCredentialsException

    token = create_access_token(data=user)
    return Token(access_token=token, token_type="bearer")


@AuthRouter.get("/prueba")
async def prueba(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    return current_user
