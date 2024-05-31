from typing import Any

from pydantic import BaseModel, EmailStr, field_validator, model_validator

from models.common_models import BaseModelInDB
from utils.validation_utils import validate_password


class UserSignUp(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, password: str) -> str:
        validate_password(password)
        return password


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, password: str) -> str:
        validate_password(password)
        return password


class UserInDB(BaseModelInDB):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
