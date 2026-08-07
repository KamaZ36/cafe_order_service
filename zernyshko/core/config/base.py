from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool
    staff_provision_secret: str
    yookassa_shop_id: str
    yookassa_secret_key: str
    frontend_base_url: str

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"
