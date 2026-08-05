from dishka import Provider, Scope, provide

from zernyshko.infrastructure.file_storage.base import BaseFileStorage
from zernyshko.infrastructure.file_storage.local import LocalFileStorage


class FileStorageProvider(Provider):
    scope = Scope.APP

    @provide
    def get_file_storage_service(self) -> BaseFileStorage:
        return LocalFileStorage(folder_name="uploads")
