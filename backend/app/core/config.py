import os
import secrets
from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator


class Settings(BaseSettings):
    # Base
    API_SERVER_PROJECT_NAME: str
    ENVIRONMENT: str
    API_PREFIX: str
    MARIADB_SERVER: str
    MARIADB_DATABASE: str
    MARIADB_USER: str
    MARIADB_PASSWORD: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_SECRET_KEY: str = secrets.token_urlsafe(32)
    COOKIE_MAX_AGE_IN_MS: int

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_USERNAME: str
    FIRST_SUPERUSER_PASSWORD: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        # convert to list if is string
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    CELERY_BROKER_URL: str

    class Config:
        # env_file = Path(__file__).resolve().parent.parent.parent.parent / \
        #     ".env"  # get absolute path
        env_file_encoding = 'utf-8'


current_environment = os.getenv("CURRENT_ENVIRONMENT", "")
if current_environment != 'DOCKER':
    dev_path = Path(__file__).resolve().parent.parent.parent.parent / \
        ".env"  # get absolute path
    settings = Settings(_env_file=dev_path, _env_file_encoding='utf-8')
else:
    settings = Settings()  # get value from OS environment variables
