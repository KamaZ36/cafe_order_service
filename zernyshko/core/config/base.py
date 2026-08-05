from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool
    staff_provision_secret: str

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"
