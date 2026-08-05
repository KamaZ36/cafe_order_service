from httpx import AsyncClient


async def test_get_category_list_empty(client: AsyncClient) -> None:
    response = await client.get("/categories")

    assert response.status_code == 200
    assert response.json() == []


async def test_staff_can_create_and_list_category(staff_client: AsyncClient) -> None:
    response = await staff_client.post("/categories", json={"category_name": "Напитки"})
    assert response.status_code == 200
    category = response.json()
    assert category["name"] == "Напитки"

    response = await staff_client.get("/categories")
    assert [c["id"] for c in response.json()] == [category["id"]]


async def test_get_product_list_filters_by_category(
    client: AsyncClient, staff_client: AsyncClient, category_id: str, product_id: str
) -> None:
    other_category = await staff_client.post(
        "/categories", json={"category_name": "Выпечка"}
    )
    other_category_id = other_category.json()["id"]

    response = await client.get(
        "/products", params={"limit": 10, "offset": 0, "category_id": category_id}
    )
    body = response.json()
    assert body["total_count"] == 1
    assert body["products"][0]["id"] == product_id

    response = await client.get(
        "/products", params={"limit": 10, "offset": 0, "category_id": other_category_id}
    )
    assert response.json()["total_count"] == 0


async def test_get_product_by_id(client: AsyncClient, product_id: str) -> None:
    response = await client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Кофе"


async def test_update_product_requires_staff(
    client: AsyncClient,
    staff_client: AsyncClient,
    manager_client: AsyncClient,
    category_id: str,
    product_id: str,
) -> None:
    update_data = {
        "name": "Кофе",
        "description": "Черный кофе",
        "weight": "200мл",
        "category_id": category_id,
        "price": "150.00",
        "is_available": "true",
        "is_popular": "false",
        "is_new": "false",
    }

    response = await client.patch(f"/products/{product_id}", data=update_data)
    assert response.status_code == 401

    await client.post("/users", json={"phone_number": "+70000000009"})
    response = await client.patch(f"/products/{product_id}", data=update_data)
    assert response.status_code == 403

    # MANAGER отвечает за меню наравне с ADMIN
    response = await manager_client.patch(f"/products/{product_id}", data=update_data)
    assert response.status_code == 200

    response = await staff_client.patch(f"/products/{product_id}", data=update_data)
    assert response.status_code == 200


async def test_update_product_changes_fields(
    staff_client: AsyncClient, category_id: str, product_id: str
) -> None:
    response = await staff_client.patch(
        f"/products/{product_id}",
        data={
            "name": "Латте",
            "description": "Кофе с молоком",
            "weight": "300мл",
            "category_id": category_id,
            "price": "250.00",
            "is_available": "false",
            "is_popular": "true",
            "is_new": "true",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Латте"
    assert body["price"] == "250.00"
    assert body["is_available"] is False
    assert body["is_popular"] is True
    assert body["is_new"] is True

    response = await staff_client.get(f"/products/{product_id}")
    assert response.json()["name"] == "Латте"


async def test_update_product_rejects_duplicate_name(
    staff_client: AsyncClient, category_id: str, product_id: str
) -> None:
    # Второй товар заводим напрямую в БД, минуя эндпоинт создания — тот
    # требует реальную загрузку файла в файловое хранилище, не нужную
    # для проверки конфликта имён.
    from decimal import Decimal
    from uuid import uuid4

    from zernyshko.infrastructure.database.connection import async_session_maker
    from zernyshko.infrastructure.database.models.product import PRODUCT_TABLE

    async with async_session_maker() as session:
        await session.execute(
            PRODUCT_TABLE.insert().values(
                id=uuid4(),
                name="Чай",
                description="Черный чай",
                weight="200мл",
                category_id=category_id,
                price=Decimal("100.00"),
                image=None,
                is_available=True,
                is_popular=False,
                is_new=False,
            )
        )
        await session.commit()

    response = await staff_client.patch(
        f"/products/{product_id}",
        data={
            "name": "Чай",
            "description": "Черный кофе",
            "weight": "200мл",
            "category_id": category_id,
            "price": "150.00",
            "is_available": "true",
            "is_popular": "false",
            "is_new": "false",
        },
    )
    assert response.status_code == 409
    assert response.json()["error_code"] == "PRODUCT_WITH_NAME_ALREADY_EXIST"


async def test_delete_product_requires_staff(
    client: AsyncClient, staff_client: AsyncClient, product_id: str
) -> None:
    response = await client.delete(f"/products/{product_id}")
    assert response.status_code == 401

    await client.post("/users", json={"phone_number": "+70000000005"})
    response = await client.delete(f"/products/{product_id}")
    assert response.status_code == 403

    response = await staff_client.delete(f"/products/{product_id}")
    assert response.status_code == 200
