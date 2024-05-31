from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    MONGO_URL: SecretStr
    DATABASE_NAME: str
    SECRET_KEY: SecretStr
    ALGORITHM: Literal["HS256"]
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_config() -> Config:
    return Config()  # type: ignore[call-arg]
