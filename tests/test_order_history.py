from httpx import AsyncClient

from tests.helpers import set_phone_number


async def test_order_history_requires_session(client: AsyncClient) -> None:
    response = await client.get("/users/@me/orders")
    assert response.status_code == 401


async def test_order_history_empty_when_no_orders(client: AsyncClient) -> None:
    await client.post("/users", json={"phone_number": "+70000002001"})

    response = await client.get("/users/@me/orders")
    assert response.status_code == 200
    body = response.json()
    assert body["total_count"] == 0
    assert body["orders"] == []


async def test_order_history_lists_created_order_with_items(
    client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 2}
    )
    await set_phone_number(client, "+70000002002")
    await client.post(
        "/users/@me/orders/pickup",
        json={"desired_time": "2026-08-10T12:00:00+03:00", "comment": "тест"},
    )

    response = await client.get("/users/@me/orders")
    assert response.status_code == 200
    body = response.json()
    assert body["total_count"] == 1

    order = body["orders"][0]
    assert order["status"] == "PENDING"
    assert order["comment"] == "тест"
    assert len(order["items"]) == 1
    assert order["items"][0]["product_id"] == product_id
    assert order["items"][0]["quantity"] == 2


async def test_order_numbers_are_not_hardcoded(
    client: AsyncClient, product_id: str
) -> None:
    await set_phone_number(client, "+70000002003")

    for _ in range(2):
        await client.post(
            "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
        )
        await client.post(
            "/users/@me/orders/pickup",
            json={"desired_time": "2026-08-10T12:00:00+03:00"},
        )

    response = await client.get("/users/@me/orders")
    order_numbers = {order["order_number"] for order in response.json()["orders"]}
    assert len(order_numbers) == 2
