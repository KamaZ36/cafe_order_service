import aiofiles

from pathlib import Path
from anyio import Path as AsyncPath, to_thread

from typing import BinaryIO

from src.infrastructure.file_storage.base import BaseFileStorage


class LocalFileStorage(BaseFileStorage):
    def __init__(self, folder_name: str) -> None:
        self._project_root = Path(__file__).resolve().parent.parent.parent.parent
        self._upload_dir: Path = self._project_root / folder_name
        self._upload_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, content: BinaryIO, filekey: str) -> None:
        full_path = self._upload_dir / filekey
        await AsyncPath(full_path.parent).mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(full_path, mode="wb") as out_file:
            content.seek(0)
            while chunk := await self._async_read(content, 1024 * 1024):
                await out_file.write(chunk)

        content.close()

    async def _async_read(self, file: BinaryIO, size: int = -1) -> bytes:
        return await to_thread.run_sync(file.read, size)
