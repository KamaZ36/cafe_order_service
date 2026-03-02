from pathlib import Path
from uuid import UUID, uuid4

from src.app.dtos.file import FileDTO
from src.infrastructure.file_storage.base import BaseFileStorage


class ProductService:
    def __init__(self, file_storage: BaseFileStorage) -> None:
        self.file_storage = file_storage

    async def save_product_image(self, image: FileDTO, product_id: UUID) -> str:
        """Сохранит картинку продукта и вернет путь/ключ"""

        extension = Path(image.name).suffix
        file_key = f"products/{product_id}/{uuid4()}{extension}"

        await self.file_storage.save(content=image.file, filekey=file_key)

        return file_key
