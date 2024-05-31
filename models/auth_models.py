from typing import Any

from pydantic import BaseModel, EmailStr, field_validator, model_validator

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


class UserInDB(BaseModel):
    id: str
    email: EmailStr
    password: str

    @model_validator(mode="before")
    @classmethod
    def rename_id_field(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data.get("_id") is not None:
                data["id"] = str(data["_id"])
                del data["_id"]
                return data
        return data


class Token(BaseModel):
    access_token: str
    token_type: str
