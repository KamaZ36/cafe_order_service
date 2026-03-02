from dishka import make_async_container

from src.core.dependencies.file_storage import FileStorageProvider
from src.core.dependencies.database import DatabaseProvider
from src.core.dependencies.repositories import RepositoriesProvider
from src.core.dependencies.services import ServicesProvider
from src.core.dependencies.interactors import InteractorsProvider


container = make_async_container(
    DatabaseProvider(),
    RepositoriesProvider(),
    ServicesProvider(),
    FileStorageProvider(),
    InteractorsProvider(),
)
