from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import JSONResponse

from zernyshko.api.v1.schemas.product import GetProductListSchema, ProductResponseSchema
from zernyshko.app.dtos.file import FileDTO
from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.dtos.product import ResponseProductDTO, ResponseProductListDTO
from zernyshko.app.interactors.product.create_product import (
    CreateProductCommand,
    CreateProductInteractor,
)
from zernyshko.app.interactors.product.delete_product import (
    DeleteProductCommand,
    DeleteProductInteractor,
)
from zernyshko.app.interactors.product.get_product import (
    GetProductByIdInteractor,
    GetProductByIdQuery,
)
from zernyshko.app.interactors.product.get_products import (
    GetProductListInteractor,
    GetProductListQuery,
)
from zernyshko.app.interactors.product.update_product import (
    UpdateProductCommand,
    UpdateProductInteractor,
)
from zernyshko.core.dependencies import container

router = APIRouter()


@router.post("", description="Создать продукт.")
async def create_product(
    request: Request,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    weight: Annotated[str, Form()],
    category_id: Annotated[UUID, Form()],
    price: Annotated[str, Form()],
    is_available: Annotated[bool, Form()],
    is_popular: Annotated[bool, Form()],
    is_new: Annotated[bool, Form()],
    file: UploadFile,
) -> ProductResponseSchema:
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Файл должен быть картинкой.")

    command = CreateProductCommand(
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

    async with container(context={Request: request}) as context:
        interactor = await context.get(CreateProductInteractor)
        product = await interactor(command)

    return ProductResponseSchema.model_validate(product)


@router.get("", description="Получить список продуктов по фильтрам")
async def get_product_list(
    data: GetProductListSchema = Query(...),
) -> ResponseProductListDTO:
    query = GetProductListQuery(
        pagination=Pagination(limit=data.limit, offset=data.offset),
        search=data.search,
        category_id=data.category_id,
    )
    async with container() as context:
        interactor = await context.get(GetProductListInteractor)
        products = await interactor(query)
    return products


@router.get("/{product_id}", description="Получить информацию о товаре по его ID")
async def get_product_by_id(product_id: UUID) -> ResponseProductDTO:
    query = GetProductByIdQuery(product_id=product_id)

    async with container() as context:
        interactor = await context.get(GetProductByIdInteractor)
        product = await interactor(query)

    return product


@router.patch("/{product_id}", description="Обновить товар.")
async def update_product(
    product_id: UUID,
    request: Request,
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    weight: Annotated[str, Form()],
    category_id: Annotated[UUID, Form()],
    price: Annotated[str, Form()],
    is_available: Annotated[bool, Form()],
    is_popular: Annotated[bool, Form()],
    is_new: Annotated[bool, Form()],
    file: Annotated[UploadFile | None, File()] = None,
) -> ProductResponseSchema:
    file_dto = None
    if file is not None and file.filename:
        if not file.content_type.startswith("image/"):
            raise HTTPException(400, "Файл должен быть картинкой.")
        file_dto = FileDTO(file=file.file, name=file.filename, size=file.size)

    command = UpdateProductCommand(
        product_id=product_id,
        name=name,
        description=description,
        weight=weight,
        category_id=category_id,
        price=Decimal(price),
        is_available=is_available,
        is_popular=is_popular,
        is_new=is_new,
        file=file_dto,
    )

    async with container(context={Request: request}) as context:
        interactor = await context.get(UpdateProductInteractor)
        product = await interactor(command)

    return ProductResponseSchema.model_validate(product)


@router.delete("/{product_id}", description="Удалить товар по его ID")
async def delete_product(product_id: UUID, request: Request) -> JSONResponse:
    command = DeleteProductCommand(product_id=product_id)

    async with container(context={Request: request}) as context:
        interactor = await context.get(DeleteProductInteractor)
        await interactor(command)

    return JSONResponse(status_code=200, content={"product_id": str(product_id)})
