from dishka import make_async_container

from zernyshko.core.dependencies.database import DatabaseProvider
from zernyshko.core.dependencies.file_storage import FileStorageProvider
from zernyshko.core.dependencies.identity_provider import IdentityProviderProvider
from zernyshko.core.dependencies.interactors import InteractorsProvider
from zernyshko.core.dependencies.reader import ReaderProvider
from zernyshko.core.dependencies.repositories import RepositoriesProvider
from zernyshko.core.dependencies.services import ServicesProvider

container = make_async_container(
    DatabaseProvider(),
    RepositoriesProvider(),
    ReaderProvider(),
    ServicesProvider(),
    FileStorageProvider(),
    IdentityProviderProvider(),
    InteractorsProvider(),
)
