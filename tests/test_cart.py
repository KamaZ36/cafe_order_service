from httpx import AsyncClient


async def test_get_cart_without_session_returns_empty_cart(client: AsyncClient) -> None:
    response = await client.get("/users/@me/cart")

    assert response.status_code == 200
    assert response.json() == {
        "id": None,
        "total_items": 0,
        "total_price": "0",
        "items": [],
    }


async def test_update_cart_item_without_session_is_not_found(client: AsyncClient) -> None:
    response = await client.patch(
        "/users/@me/cart/items/00000000-0000-0000-0000-000000000000/quantity",
        json={"quantity": 5},
    )

    assert response.status_code == 404
    assert response.json()["error_code"] == "PRODUCT_NOT_EXIST_IN_CART"


async def test_add_unknown_product_to_cart_is_not_found(client: AsyncClient) -> None:
    response = await client.post(
        "/users/@me/cart/items",
        json={"product_id": "00000000-0000-0000-0000-000000000000", "quantity": 1},
    )

    assert response.status_code == 404
    assert response.json()["error_code"] == "PRODUCT_NOT_FOUND"


async def test_add_item_to_cart_bootstraps_anonymous_session(
    client: AsyncClient, product_id: str
) -> None:
    response = await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 2}
    )

    assert response.status_code == 200
    assert "session_id" in response.cookies

    response = await client.get("/users/@me/cart")
    body = response.json()
    assert body["total_items"] == 1  # distinct cart lines, not summed quantity
    assert body["items"][0]["product_id"] == product_id
    assert body["items"][0]["quantity"] == 2


async def test_add_item_twice_increases_quantity(
    client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 2}
    )

    response = await client.get("/users/@me/cart")
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["quantity"] == 3


async def test_update_cart_item_quantity(client: AsyncClient, product_id: str) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )

    response = await client.patch(
        f"/users/@me/cart/items/{product_id}/quantity", json={"quantity": 5}
    )
    assert response.status_code == 200

    response = await client.get("/users/@me/cart")
    assert response.json()["items"][0]["quantity"] == 5


async def test_update_cart_item_quantity_to_zero_removes_item(
    client: AsyncClient, product_id: str
) -> None:
    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )

    response = await client.patch(
        f"/users/@me/cart/items/{product_id}/quantity", json={"quantity": 0}
    )
    assert response.status_code == 200

    response = await client.get("/users/@me/cart")
    assert response.json()["items"] == []


async def test_two_anonymous_visitors_do_not_share_a_cart(
    client: AsyncClient, app, product_id: str
) -> None:
    from httpx import ASGITransport

    await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as other_client:
        response = await other_client.get("/users/@me/cart")
        assert response.json() == {
            "id": None,
            "total_items": 0,
            "total_price": "0",
            "items": [],
        }
