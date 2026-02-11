from fastapi import APIRouter

from src.domain.entities.product import Product

from src.app.interactors.product.create_product import (
    CreateProductCommand,
    CreateProductInteractor,
)

from src.core.dependencies import container
from src.api.v1.schemas.product import CreateProductSchema


router = APIRouter()


@router.post("", description="Создать продукт.")
async def create_product(data: CreateProductSchema) -> Product:
    command = CreateProductCommand(
        user_id=data.user_id,
        name=data.name,
        description=data.description,
        weight=data.weight,
        category_id=data.category_id,
        price=data.price,
        is_available=data.is_available,
        is_popular=data.is_popular,
        is_new=data.is_new,
    )
    async with container() as context:
        interactor = await context.get(CreateProductInteractor)
        product = await interactor(command)

    return product
