from dishka import Provider, provide, Scope

from infrastructure.file_storage.local import LocalFileStorage
from infrastructure.file_storage.base import BaseFileStorage


class FileStorageProvider(Provider):
    scope = Scope.APP

    @provide
    def get_file_storage_service(self) -> BaseFileStorage:
        return LocalFileStorage(folder_name="uploads")
