from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"
