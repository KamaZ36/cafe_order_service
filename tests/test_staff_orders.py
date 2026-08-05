from httpx import AsyncClient

from tests.helpers import get_latest_order_id, set_phone_number


async def test_get_staff_orders_requires_session(client: AsyncClient) -> None:
    response = await client.get("/orders")
    assert response.status_code == 401


async def test_get_staff_orders_requires_staff_role(client: AsyncClient) -> None:
    await client.post("/users", json={"phone_number": "+70000003001"})

    response = await client.get("/orders")
    assert response.status_code == 403
    assert response.json()["error_code"] == "ACCESS_DENIED"


async def test_staff_sees_orders_from_other_customers(
    client: AsyncClient, staff_client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await set_phone_number(client, "+70000003002")
    await client.post(
        "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
    )
    order_id = await get_latest_order_id(status="PENDING")

    # Своей сессией у бариста этого заказа быть не может — он от другого клиента
    response = await staff_client.get("/orders", params={"limit": 50, "offset": 0})
    assert response.status_code == 200
    orders_by_id = {order["id"]: order for order in response.json()["orders"]}
    assert order_id in orders_by_id
    assert orders_by_id[order_id]["customer_phone_number"] == "+70000003002"


async def test_staff_orders_filter_by_status(
    client: AsyncClient, staff_client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await set_phone_number(client, "+70000003003")
    await client.post(
        "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
    )
    order_id = await get_latest_order_id(status="PENDING")
    await staff_client.patch(f"/orders/{order_id}/confirm")

    response = await staff_client.get(
        "/orders", params={"limit": 50, "offset": 0, "status": "PENDING"}
    )
    assert order_id not in {order["id"] for order in response.json()["orders"]}

    response = await staff_client.get(
        "/orders", params={"limit": 50, "offset": 0, "status": "CONFIRMED"}
    )
    assert order_id in {order["id"] for order in response.json()["orders"]}


async def test_staff_orders_queue_is_oldest_first(
    client: AsyncClient, staff_client: AsyncClient, product_id: str
) -> None:
    await set_phone_number(client, "+70000003004")

    created_ids = []
    for _ in range(2):
        await client.post(
            "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
        )
        await client.post(
            "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
        )
        created_ids.append(await get_latest_order_id(status="PENDING"))

    response = await staff_client.get("/orders", params={"limit": 50, "offset": 0})
    order_ids = [order["id"] for order in response.json()["orders"]]
    positions = [order_ids.index(order_id) for order_id in created_ids]
    assert positions == sorted(positions)


async def test_staff_cancel_requires_staff_role(client: AsyncClient) -> None:
    response = await client.patch(
        "/orders/00000000-0000-0000-0000-000000000000/cancel"
    )
    assert response.status_code == 401

    await client.post("/users", json={"phone_number": "+70000003005"})
    response = await client.patch(
        "/orders/00000000-0000-0000-0000-000000000000/cancel"
    )
    assert response.status_code == 403


async def test_staff_can_cancel_pending_order_with_reason(
    client: AsyncClient, staff_client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await set_phone_number(client, "+70000003006")
    await client.post(
        "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
    )
    order_id = await get_latest_order_id(status="PENDING")

    response = await staff_client.patch(
        f"/orders/{order_id}/cancel", json={"reason": "Клиент не отвечает"}
    )
    assert response.status_code == 200

    response = await staff_client.get("/orders", params={"limit": 50, "offset": 0})
    order = next(o for o in response.json()["orders"] if o["id"] == order_id)
    assert order["status"] == "CANCELLED"
    assert order["cancel_reason"] == "Клиент не отвечает"


async def test_staff_can_cancel_confirmed_and_ready_order_without_reason(
    client: AsyncClient, staff_client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await set_phone_number(client, "+70000003007")
    await client.post(
        "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
    )
    order_id = await get_latest_order_id(status="PENDING")
    await staff_client.patch(f"/orders/{order_id}/confirm")
    await staff_client.patch(f"/orders/{order_id}/ready")

    response = await staff_client.patch(f"/orders/{order_id}/cancel")
    assert response.status_code == 200

    response = await staff_client.get("/orders", params={"limit": 50, "offset": 0})
    order = next(o for o in response.json()["orders"] if o["id"] == order_id)
    assert order["status"] == "CANCELLED"
    assert order["cancel_reason"] is None


async def test_staff_cannot_cancel_completed_order(
    client: AsyncClient, staff_client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await set_phone_number(client, "+70000003008")
    await client.post(
        "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
    )
    order_id = await get_latest_order_id(status="PENDING")
    await staff_client.patch(f"/orders/{order_id}/confirm")
    await staff_client.patch(f"/orders/{order_id}/ready")
    await staff_client.patch(f"/orders/{order_id}/complete")

    response = await staff_client.patch(f"/orders/{order_id}/cancel")
    assert response.status_code == 409
    assert response.json()["error_code"] == "INVALID_ORDER_STATUS_TRANSITION"
