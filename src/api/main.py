import uvicorn

from fastapi import FastAPI


from src.api.v1.endpoints import user_router, product_router, category_router
from src.api.lifespan import lifespan


def include_router(app: FastAPI) -> None:
    app.include_router(user_router, prefix="/users", tags=["Пользователи"])
    app.include_router(product_router, prefix="/products", tags=["Продукты"])
    app.include_router(category_router, prefix="/categories", tags=["Категории"])


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    include_router(app=app)

    return app


if __name__ == "__main__":
    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=8000)
