from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()  # secrets_dir="./secrets")

    storage_account: str = Field(min_length=1)
    container_name: str = Field(min_length=1)

    engine: str = "fastparquet"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
