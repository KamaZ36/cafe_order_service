from uuid import UUID

from fastapi import APIRouter, Request

from zernyshko.api.v1.schemas.category import (
    CategoryResponseSchema,
    CreateCategorySchema,
    UpdateCategorySchema,
)
from zernyshko.app.interactors.category.create_category import (
    CreateCategoryCommand,
    CreateCategoryInteractor,
)
from zernyshko.app.interactors.category.delete_category import (
    DeleteCategoryCommand,
    DeleteCategoryInteractor,
)
from zernyshko.app.interactors.category.get_categories import GetCategoryListInteractor
from zernyshko.app.interactors.category.update_category import (
    UpdateCategoryCommand,
    UpdateCategoryInteractor,
)
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


@router.delete(
    "/{category_id}",
    description="Удалить категорию. Нельзя, если в ней остались товары.",
)
async def delete_category(category_id: UUID, request: Request) -> None:
    command = DeleteCategoryCommand(category_id=category_id)
    async with container(context={Request: request}) as context:
        interactor = await context.get(DeleteCategoryInteractor)
        await interactor(command)


@router.get("", description="Получить список категорий.")
async def get_category_list() -> list[CategoryResponseSchema]:
    async with container() as context:
        interactor = await context.get(GetCategoryListInteractor)
        categories = await interactor()
    return [CategoryResponseSchema.model_validate(category) for category in categories]


@router.patch("/{category_id}", description="Переименовать категорию.")
async def update_category(
    category_id: UUID, data: UpdateCategorySchema, request: Request
) -> CategoryResponseSchema:
    command = UpdateCategoryCommand(category_id=category_id, name=data.category_name)
    async with container(context={Request: request}) as context:
        interactor = await context.get(UpdateCategoryInteractor)
        category = await interactor(command)
    return CategoryResponseSchema.model_validate(category)
