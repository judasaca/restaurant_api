from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    MONGO_URL: SecretStr
    DATABASE_NAME: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_config() -> Config:
    return Config()  # type: ignore[call-arg]
