from pydantic import BaseModel, EmailStr, field_validator

from utils import validate_password


class UserSignUp(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, password: str) -> str:
        validate_password(password)
        return password
