from httpx import ASGITransport, AsyncClient

from tests.helpers import get_phone_verification_code, store_phone_verification_code


async def test_send_code_then_login_with_correct_code(client: AsyncClient) -> None:
    phone_number = "+70000001001"

    response = await client.post("/users/phone/code", json={"phone_number": phone_number})
    assert response.status_code == 200

    code = await get_phone_verification_code(phone_number)

    response = await client.post(
        "/users/phone/login", json={"phone_number": phone_number, "code": code}
    )
    assert response.status_code == 200
    assert "session_id" in response.cookies

    response = await client.get("/users/@me")
    assert response.status_code == 200
    assert response.json()["phone_number"] == phone_number


async def test_login_with_wrong_code_is_rejected(client: AsyncClient) -> None:
    phone_number = "+70000001002"
    await client.post("/users/phone/code", json={"phone_number": phone_number})

    response = await client.post(
        "/users/phone/login", json={"phone_number": phone_number, "code": "000000"}
    )
    assert response.status_code == 400
    assert response.json()["error_code"] == "AUTH_CODE_NOT_VALID"


async def test_login_without_sending_code_first_is_rejected(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/users/phone/login",
        json={"phone_number": "+70000001003", "code": "123456"},
    )
    assert response.status_code == 400
    assert response.json()["error_code"] == "AUTH_CODE_NOT_VALID"


async def test_code_is_single_use(client: AsyncClient) -> None:
    phone_number = "+70000001004"
    await client.post("/users/phone/code", json={"phone_number": phone_number})
    code = await get_phone_verification_code(phone_number)

    first = await client.post(
        "/users/phone/login", json={"phone_number": phone_number, "code": code}
    )
    assert first.status_code == 200

    second = await client.post(
        "/users/phone/login", json={"phone_number": phone_number, "code": code}
    )
    assert second.status_code == 400
    assert second.json()["error_code"] == "AUTH_CODE_NOT_VALID"


async def test_send_code_cooldown_rate_limit(client: AsyncClient) -> None:
    phone_number = "+70000001005"

    first = await client.post("/users/phone/code", json={"phone_number": phone_number})
    assert first.status_code == 200

    second = await client.post("/users/phone/code", json={"phone_number": phone_number})
    assert second.status_code == 429
    assert second.json()["error_code"] == "RATE_LIMIT_EXCEEDED"


async def test_verify_code_attempts_are_rate_limited(client: AsyncClient) -> None:
    phone_number = "+70000001006"
    await client.post("/users/phone/code", json={"phone_number": phone_number})

    for _ in range(5):
        response = await client.post(
            "/users/phone/login", json={"phone_number": phone_number, "code": "000000"}
        )
        assert response.status_code == 400

    response = await client.post(
        "/users/phone/login", json={"phone_number": phone_number, "code": "000000"}
    )
    assert response.status_code == 429
    assert response.json()["error_code"] == "RATE_LIMIT_EXCEEDED"


async def test_login_with_phone_of_existing_account_logs_into_it(
    client: AsyncClient, app
) -> None:
    phone_number = "+70000001007"

    # первая сессия привязывает телефон к своему (анонимному) аккаунту
    await client.post("/users/phone/code", json={"phone_number": phone_number})
    code = await get_phone_verification_code(phone_number)
    await client.post(
        "/users/phone/login", json={"phone_number": phone_number, "code": code}
    )
    original_user_id = (await client.get("/users/@me")).json()["id"]

    # вторая, полностью независимая сессия (другой браузер/устройство).
    # Код пишем напрямую в Redis — POST /users/phone/code для этого же
    # номера уже упёрся бы в cooldown 1/60с.
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as other_client:
        other_code = "111111"
        await store_phone_verification_code(phone_number, other_code)

        response = await other_client.post(
            "/users/phone/login",
            json={"phone_number": phone_number, "code": other_code},
        )
        assert response.status_code == 200
        assert "session_id" in response.cookies

        me = await other_client.get("/users/@me")
        assert me.json()["id"] == original_user_id


async def test_login_to_existing_account_does_not_merge_anonymous_cart(
    client: AsyncClient, app, product_id: str
) -> None:
    phone_number = "+70000001008"

    # первая сессия — реальный аккаунт с телефоном, ничего в корзине нет
    await client.post("/users/phone/code", json={"phone_number": phone_number})
    code = await get_phone_verification_code(phone_number)
    await client.post(
        "/users/phone/login", json={"phone_number": phone_number, "code": code}
    )

    # вторая сессия — анонимная корзина с товаром, затем вход тем же телефоном
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as other_client:
        await other_client.post(
            "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
        )
        cart_before_login = await other_client.get("/users/@me/cart")
        assert cart_before_login.json()["items"] != []

        other_code = "222222"
        await store_phone_verification_code(phone_number, other_code)
        await other_client.post(
            "/users/phone/login",
            json={"phone_number": phone_number, "code": other_code},
        )

        cart_after_login = await other_client.get("/users/@me/cart")
        assert cart_after_login.json()["items"] == []
