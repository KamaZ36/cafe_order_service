from fastapi import APIRouter

from src.domain.entities.category import Category

from src.app.interactors.category.create_category import (
    CreateCategoryCommand,
    CreateCategoryInteractor,
)

from src.api.v1.schemas.category import CreateCategorySchema
from src.core.dependencies import container


router = APIRouter()


@router.post("", description="Создать категорию.")
async def create_category(data: CreateCategorySchema) -> Category:
    command = CreateCategoryCommand(user_id=data.user_id, name=data.category_name)
    async with container() as context:
        interactor = await context.get(CreateCategoryInteractor)
        category = await interactor(command)
    return category
