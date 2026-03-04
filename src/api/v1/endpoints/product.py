from decimal import Decimal
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, UploadFile, Form
from fastapi.responses import JSONResponse

from app.interactors.product.get_product import (
    GetProductByIdInteractor,
    GetProductByIdQuery,
)
from app.dtos.product import ResponseProductDTO
from app.interactors.product.delete_product import (
    DeleteProductCommand,
    DeleteProductInteractor,
)
from app.dtos.file import FileDTO
from domain.entities.product import Product

from app.interactors.product.create_product import (
    CreateProductCommand,
    CreateProductInteractor,
)

from core.dependencies import container

router = APIRouter()


@router.post("", description="Создать продукт.")
async def create_product(
    name: Annotated[str, Form],
    description: Annotated[str, Form],
    weight: Annotated[str, Form],
    category_id: Annotated[UUID, Form],
    price: Annotated[str, Form],
    is_available: Annotated[bool, Form],
    is_popular: Annotated[bool, Form],
    is_new: Annotated[bool, Form],
    file: UploadFile,
) -> Product:
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Файл должен быть картинкой.")

    command = CreateProductCommand(
        user_id=uuid4(),
        name=name,
        description=description,
        weight=weight,
        category_id=category_id,
        price=Decimal(price),
        is_available=is_available,
        is_popular=is_popular,
        is_new=is_new,
        file=FileDTO(file=file.file, name=file.filename, size=file.size),
    )

    async with container() as context:
        interactor = await context.get(CreateProductInteractor)
        product = await interactor(command)

    return product


@router.get("/{product_id}", description="Получить информацию о товаре по его ID")
async def get_product_by_id(product_id: UUID) -> ResponseProductDTO:
    query = GetProductByIdQuery(product_id=product_id)

    async with container() as context:
        interactor = await context.get(GetProductByIdInteractor)
        product = await interactor(query)

    return product


@router.delete("/{product_id}", description="Удалить товар по его ID")
async def delete_product(product_id: UUID) -> JSONResponse:
    command = DeleteProductCommand(user_id=uuid4(), product_id=product_id)

    async with container() as context:
        interactor = await context.get(DeleteProductInteractor)
        await interactor(command)

    return JSONResponse(status_code=200, content={"product_id": str(product_id)})
