from src.core.config.base import Settings
from src.core.config.database import DatabaseSettings


class AppSettings(Settings, DatabaseSettings):
    pass


settings = AppSettings()
