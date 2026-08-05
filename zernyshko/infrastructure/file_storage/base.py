from abc import ABC, abstractmethod
from typing import BinaryIO


class BaseFileStorage(ABC):
    @abstractmethod
    async def save(self, content: BinaryIO, filekey: str) -> str:
        raise NotImplementedError()
