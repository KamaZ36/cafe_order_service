from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoryResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class CreateCategorySchema(BaseModel):
    category_name: str


class UpdateCategorySchema(BaseModel):
    category_name: str
