import os
import secrets
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import toml
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
    FIRST_USER_EMAIL: EmailStr
    FIRST_USER_USERNAME: str
    FIRST_USER_PASSWORD: str

    LOOKUP_TYPE_STATUS: str
    LOOKUP_TYPE_VULNERABILITY_TYPE: str
    LOOKUP_TYPE_SEVERITY_LEVEL: str
    TASK_SECRET_KEY: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    PROJECT_NAME: str
    # SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/backend/app/email-templates"
    EMAILS_ENABLED: bool = False

    VITE_CONSOLE_PANEL_URL: AnyHttpUrl

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

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


def get_version() -> str:
    tomlFilePath = Path(__file__).resolve().parent.parent.parent / \
        "pyproject.toml"
    pyproject = toml.load(tomlFilePath)
    version = pyproject['tool']['poetry']['version']
    return version
