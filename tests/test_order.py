from httpx import AsyncClient

from tests.helpers import get_latest_order_id, pay_latest_order, set_phone_number


async def test_create_order_without_phone_number_is_rejected(
    client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )

    response = await client.post(
        "/users/@me/orders/pickup",
        json={"desired_time": "2026-08-10T12:00:00+03:00", "comment": "test"},
    )
    assert response.status_code == 400
    assert response.json()["error_code"] == "USER_PHONE_NUMBER_REQUIRED"


async def test_confirm_order_without_session_is_unauthorized(client: AsyncClient) -> None:
    response = await client.patch("/orders/00000000-0000-0000-0000-000000000000/confirm")
    assert response.status_code == 401


async def test_create_order_clears_cart_and_can_be_managed_by_staff(
    client: AsyncClient, staff_client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 2}
    )
    await set_phone_number(client, "+70000000020")

    response = await client.post(
        "/users/@me/orders/pickup",
        json={"desired_time": "2026-08-10T12:00:00+03:00", "comment": "test order"},
    )
    assert response.status_code == 200

    response = await client.get("/users/@me/cart")
    assert response.json()["items"] == []

    await pay_latest_order(client)
    order_id = await get_latest_order_id(status="PENDING")

    response = await client.patch(f"/orders/{order_id}/confirm")
    assert response.status_code == 403

    response = await staff_client.patch(f"/orders/{order_id}/confirm")
    assert response.status_code == 200

    response = await staff_client.patch(f"/orders/{order_id}/ready")
    assert response.status_code == 200

    response = await staff_client.patch(f"/orders/{order_id}/complete")
    assert response.status_code == 200

    response = await client.patch(f"/users/@me/orders/{order_id}/cancel")
    assert response.status_code == 409
    assert response.json()["error_code"] == "INVALID_ORDER_STATUS_TRANSITION"


async def test_customer_can_cancel_own_pending_order(
    client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await set_phone_number(client, "+70000000021")
    await client.post(
        "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
    )

    await pay_latest_order(client)
    order_id = await get_latest_order_id(status="PENDING")

    response = await client.patch(f"/users/@me/orders/{order_id}/cancel")
    assert response.status_code == 200


async def test_customer_can_cancel_own_order_awaiting_payment(
    client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await set_phone_number(client, "+70000000023")
    await client.post(
        "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
    )

    order_id = await get_latest_order_id(status="AWAITING_PAYMENT")

    response = await client.patch(f"/users/@me/orders/{order_id}/cancel")
    assert response.status_code == 200


async def test_simulate_payment_moves_order_into_staff_queue(
    client: AsyncClient, staff_client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await set_phone_number(client, "+70000000024")
    await client.post(
        "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
    )
    order_id = await get_latest_order_id(status="AWAITING_PAYMENT")

    response = await client.post(f"/users/@me/orders/{order_id}/simulate-payment")
    assert response.status_code == 200

    order_id_after = await get_latest_order_id(status="PENDING")
    assert order_id_after == order_id

    response = await staff_client.get("/orders", params={"limit": 50, "offset": 0})
    assert order_id in {o["id"] for o in response.json()["orders"]}


async def test_simulate_payment_requires_session(client: AsyncClient) -> None:
    response = await client.post(
        "/users/@me/orders/00000000-0000-0000-0000-000000000000/simulate-payment"
    )
    assert response.status_code == 401


async def test_simulate_payment_rejects_someone_elses_order(
    client: AsyncClient, app, product_id: str
) -> None:
    from httpx import ASGITransport

    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await set_phone_number(client, "+70000000025")
    await client.post(
        "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
    )
    order_id = await get_latest_order_id(status="AWAITING_PAYMENT")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as other_client:
        await set_phone_number(other_client, "+70000000026")
        response = await other_client.post(
            f"/users/@me/orders/{order_id}/simulate-payment"
        )
        assert response.status_code == 404
        assert response.json()["error_code"] == "ORDER_NOT_FOUND"


async def test_customer_cannot_cancel_confirmed_order(
    client: AsyncClient, staff_client: AsyncClient, product_id: str
) -> None:
    # Как только заведение подтвердило заказ, самостоятельная отмена клиентом
    # закрывается — дальше только через персонал (см. test_staff_orders.py)
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await set_phone_number(client, "+70000000022")
    await client.post(
        "/users/@me/orders/pickup", json={"desired_time": "2026-08-10T12:00:00+03:00"}
    )
    await pay_latest_order(client)
    order_id = await get_latest_order_id(status="PENDING")
    await staff_client.patch(f"/orders/{order_id}/confirm")

    response = await client.patch(f"/users/@me/orders/{order_id}/cancel")
    assert response.status_code == 409
    assert response.json()["error_code"] == "INVALID_ORDER_STATUS_TRANSITION"
