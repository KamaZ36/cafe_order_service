from httpx import AsyncClient


async def test_provision_and_login_staff(client: AsyncClient) -> None:
    response = await client.post(
        "/users/staff",
        json={"phone_number": "+70000000001", "password": "password123"},
        headers={"X-Staff-Secret": "test-secret"},
    )
    assert response.status_code == 200
    user_id = response.json()["user_id"]

    response = await client.post(
        "/users/login",
        json={"phone_number": "+70000000001", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id
    assert "session_id" in response.cookies


async def test_provision_staff_with_wrong_secret_is_forbidden(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/users/staff",
        json={"phone_number": "+70000000002", "password": "password123"},
        headers={"X-Staff-Secret": "wrong-secret"},
    )
    assert response.status_code == 403


async def test_login_with_wrong_password_is_rejected(client: AsyncClient) -> None:
    await client.post(
        "/users/staff",
        json={"phone_number": "+70000000003", "password": "password123"},
        headers={"X-Staff-Secret": "test-secret"},
    )

    response = await client.post(
        "/users/login",
        json={"phone_number": "+70000000003", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.json()["error_code"] == "INVALID_CREDENTIALS"


async def test_create_category_without_session_is_unauthorized(
    client: AsyncClient,
) -> None:
    response = await client.post("/categories", json={"category_name": "Test"})
    assert response.status_code == 401
    assert response.json()["error_code"] == "UNAUTHORIZED"


async def test_create_category_as_non_staff_is_forbidden(client: AsyncClient) -> None:
    await client.post("/users", json={"phone_number": "+70000000004"})

    response = await client.post("/categories", json={"category_name": "Test"})
    assert response.status_code == 403
    assert response.json()["error_code"] == "ACCESS_DENIED"


async def test_get_current_user_without_session_is_unauthorized(
    client: AsyncClient,
) -> None:
    response = await client.get("/users/@me")
    assert response.status_code == 401


async def test_get_current_user_returns_staff_role(client: AsyncClient) -> None:
    await client.post(
        "/users/staff",
        json={"phone_number": "+70000000005", "password": "password123"},
        headers={"X-Staff-Secret": "test-secret"},
    )
    await client.post(
        "/users/login",
        json={"phone_number": "+70000000005", "password": "password123"},
    )

    response = await client.get("/users/@me")
    assert response.status_code == 200
    body = response.json()
    assert body["phone_number"] == "+70000000005"
    assert body["role"] == "ADMIN"


async def test_provision_manager_role(client: AsyncClient) -> None:
    await client.post(
        "/users/staff",
        json={
            "phone_number": "+70000000007",
            "password": "password123",
            "role": "MANAGER",
        },
        headers={"X-Staff-Secret": "test-secret"},
    )
    await client.post(
        "/users/login",
        json={"phone_number": "+70000000007", "password": "password123"},
    )

    response = await client.get("/users/@me")
    assert response.json()["role"] == "MANAGER"


async def test_manager_can_manage_categories(client: AsyncClient) -> None:
    # MANAGER отвечает за меню и заказы кафе — в отличие от старой роли
    # BARISTA, ему это разрешено наравне с ADMIN
    await client.post(
        "/users/staff",
        json={
            "phone_number": "+70000000008",
            "password": "password123",
            "role": "MANAGER",
        },
        headers={"X-Staff-Secret": "test-secret"},
    )
    await client.post(
        "/users/login",
        json={"phone_number": "+70000000008", "password": "password123"},
    )

    response = await client.post("/categories", json={"category_name": "Test"})
    assert response.status_code == 200


async def test_get_current_user_works_for_anonymous_session_without_phone(
    client: AsyncClient, product_id: str
) -> None:
    # Бутстрап анонимной сессии через добавление в корзину — телефона нет
    response = await client.post(
        "/users/@me/cart/items", json={"product_id": product_id, "quantity": 1}
    )
    assert response.status_code == 200

    response = await client.get("/users/@me")
    assert response.status_code == 200
    assert response.json()["phone_number"] is None


async def test_logout_clears_session(client: AsyncClient) -> None:
    await client.post("/users", json={"phone_number": "+70000000006"})
    assert (await client.get("/users/@me")).status_code == 200

    response = await client.post("/users/logout")
    assert response.status_code == 200

    response = await client.get("/users/@me")
    assert response.status_code == 401
