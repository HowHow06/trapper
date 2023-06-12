from pydantic import BaseSettings


class Settings(BaseSettings):
    # Base
    environment: str
    api_prefix: str
    mysql_database: str
    mysql_user: str
    mysql_password: str

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'