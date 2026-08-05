from zernyshko.core.config.base import Settings
from zernyshko.core.config.database import DatabaseSettings


class AppSettings(Settings, DatabaseSettings):
    pass


settings = AppSettings()
