from uuid import UUID
from pydantic import BaseModel


class CreateCategorySchema(BaseModel):
    user_id: UUID
    category_name: str
