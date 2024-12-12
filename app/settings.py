
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    port: int
    db_filename: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    api_token: str


@lru_cache
def get_settings():
    return Settings()