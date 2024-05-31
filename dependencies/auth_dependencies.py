from typing import Annotated

import jwt
import motor.motor_asyncio
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader, HTTPBearer, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from config import get_config
from models.auth_models import UserInDB
from services.auth_services import find_user_by_email


async def get_db_client(request: Request) -> motor.motor_asyncio.AsyncIOMotorDatabase:
    return request.app.state.db_client


authorization_header = APIKeyHeader(
    name="Authorization",
    description="Please provide a jwt token. Use auth/login to genere one token. It is not needed to add Bearer prefix.",
)


async def get_current_user(
    token: Annotated[str, Depends(authorization_header)],
    db_client: Annotated[
        motor.motor_asyncio.AsyncIOMotorDatabase, Depends(get_db_client)
    ],
) -> UserInDB:
    env = get_config()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, env.SECRET_KEY.get_secret_value(), algorithms=[env.ALGORITHM]
        )
        user_email: str = payload.get("email")
        if user_email is None:
            raise credentials_exception
        print(payload)
    except InvalidTokenError:
        raise credentials_exception
    user = await find_user_by_email(email=user_email, db_client=db_client)
    if user is None:
        raise credentials_exception
    return user
