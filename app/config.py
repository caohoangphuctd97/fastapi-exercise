from typing import Literal
from pydantic import validator
from pydantic_settings import BaseSettings
from pydantic.networks import MySQLDsn
import random

DEFAULT_API_PREFIX = "api"
DEFAULT_API_VERSION = "v1"


class AsyncMySQLDsn(MySQLDsn):
    default_scheme = "mysql+aiomysql"
    allowed_schemes = {"mysql+aiomysql", "mysql+aiomysql"}


class DatabaseServiceConfig(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str = "127.0.0.1"

    DATABASE_POOL_SIZE: int = 2
    DATABASE_POOL_MAX: int = 10
    DATABASE_POOL_TIMEOUT: int = 10

    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self) -> dict:
        engine_option = {
            "pool_timeout": self.DATABASE_POOL_TIMEOUT,
            "pool_size": self.DATABASE_POOL_SIZE,
            "max_overflow": self.DATABASE_POOL_MAX,
        }

        return engine_option

    @property
    def ASYNC_DATABASE_URI(self) -> AsyncMySQLDsn:
        url = AsyncMySQLDsn.build(
            scheme=AsyncMySQLDsn.default_scheme,
            username=self.DATABASE_USERNAME,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_HOST,
            path=f"{self.DATABASE_NAME}"
        )
        return url.unicode_string()


class Config(BaseSettings):
    APPLICATION_NAME: str = "FASTAPI"
    DESCRIPTION: str = "FASTAPI"

    ENVIRONMENT: Literal["dev", "qa", "prod"] = "dev"
    DEBUG: bool = False
    TESTING: bool = False
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] \
        = "INFO"

    API_VERSION: str = DEFAULT_API_VERSION
    API_PREFIX: str = DEFAULT_API_PREFIX
    SECRET_KEY: str = "NASKDHSDKBEEBS"

    db: DatabaseServiceConfig = DatabaseServiceConfig()

    @property
    def OPENAPI_PREFIX(self) -> str:
        return f"/{self.API_PREFIX}/{self.API_VERSION}"

    @validator("ENVIRONMENT")
    def _lowercase_environment(cls, v):
        return v.lower() if isinstance(v, str) else v

    @validator("LOG_LEVEL", pre=True)
    def _debug_log_level(cls, v, values, **kwargs):
        if values.get("DEBUG"):
            return "DEBUG"
        return v.upper()


config = Config()
