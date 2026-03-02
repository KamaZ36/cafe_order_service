from minio import Minio
from io import BytesIO

from src.infrastructure.file_storage.base import BaseFileStorage


class MinIOFileStorage(BaseFileStorage):
    def __init__(self, client: Minio) -> None:
        self._client = client

    async def save(self, content: bytes, filename: str):
        data_stream = BytesIO(content)

        self._client.put_object(
            bucket_name=bucket,
            object_name=filename,
            data=data_stream,
            length=len(content),
        )
