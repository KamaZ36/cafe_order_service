from fastapi import APIRouter, Request

from zernyshko.api.v1.schemas.category import CategoryResponseSchema, CreateCategorySchema
from zernyshko.app.interactors.category.create_category import (
    CreateCategoryCommand,
    CreateCategoryInteractor,
)
from zernyshko.app.interactors.category.get_categories import GetCategoryListInteractor
from zernyshko.core.dependencies import container

router = APIRouter()


@router.post("", description="Создать категорию.")
async def create_category(
    data: CreateCategorySchema, request: Request
) -> CategoryResponseSchema:
    command = CreateCategoryCommand(name=data.category_name)
    async with container(context={Request: request}) as context:
        interactor = await context.get(CreateCategoryInteractor)
        category = await interactor(command)
    return CategoryResponseSchema.model_validate(category)


@router.get("", description="Получить список категорий.")
async def get_category_list() -> list[CategoryResponseSchema]:
    async with container() as context:
        interactor = await context.get(GetCategoryListInteractor)
        categories = await interactor()
    return [CategoryResponseSchema.model_validate(category) for category in categories]
