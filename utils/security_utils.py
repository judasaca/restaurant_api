from datetime import datetime, timedelta, timezone
from typing import Dict, Union

import bcrypt
import jwt

from config import get_config
from models.auth_models import UserInDB, UserLogin

PASSWORD_ENCODING = "utf-8"


def hash_pasword(password: str) -> str:
    return bcrypt.hashpw(
        str.encode(password, encoding=PASSWORD_ENCODING), bcrypt.gensalt()
    ).decode(PASSWORD_ENCODING)


def password_is_correct(password: str, real_hashed_password: str) -> bool:
    return bcrypt.checkpw(
        str.encode(password, encoding=PASSWORD_ENCODING),
        str.encode(real_hashed_password, encoding=PASSWORD_ENCODING),
    )


def create_access_token(
    data: UserInDB, expires_delta: Union[timedelta, None] = None
) -> str:
    env = get_config()
    to_encode: Dict[str, str | datetime] = {"sub": data.id, "email": data.email}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, env.SECRET_KEY.get_secret_value(), algorithm=env.ALGORITHM
    )
    return encoded_jwt
