from dishka import make_async_container

from core.dependencies.file_storage import FileStorageProvider
from core.dependencies.database import DatabaseProvider
from core.dependencies.reader import ReaderProvider
from core.dependencies.repositories import RepositoriesProvider
from core.dependencies.services import ServicesProvider
from core.dependencies.interactors import InteractorsProvider


container = make_async_container(
    DatabaseProvider(),
    RepositoriesProvider(),
    ReaderProvider(),
    ServicesProvider(),
    FileStorageProvider(),
    InteractorsProvider(),
)
