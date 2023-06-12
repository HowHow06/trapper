from pydantic import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
    # Base
    ENVIRONMENT: str
    API_PREFIX: str
    MARIADB_DATABASE: str
    MARIADB_USER: str
    MARIADB_PASSWORD: str

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


dev_path = Path(__file__).resolve().parent.parent.parent.parent / \
    ".env"  # get absolute path
settings = Settings(_env_file=dev_path, _env_file_encoding='utf-8')
