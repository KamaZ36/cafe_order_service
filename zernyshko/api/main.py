from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from zernyshko.api.exception_handlers import register_exception_handlers
from zernyshko.api.lifespan import lifespan
from zernyshko.api.logging_middleware import RequestLoggingMiddleware
from zernyshko.api.v1.endpoints import (
    category_router,
    order_router,
    product_router,
    user_router,
)
from zernyshko.core.config import settings
from zernyshko.core.logging_config import configure_logging

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
UPLOADS_DIR = PROJECT_ROOT / "uploads"


def include_router(app: FastAPI) -> None:
    app.include_router(user_router, prefix="/users", tags=["Пользователи"])
    app.include_router(product_router, prefix="/products", tags=["Продукты"])
    app.include_router(category_router, prefix="/categories", tags=["Категории"])
    app.include_router(order_router, prefix="/orders", tags=["Заказы"])


def create_app() -> FastAPI:
    configure_logging(debug=settings.debug)

    app = FastAPI(lifespan=lifespan)

    include_router(app=app)
    register_exception_handlers(app=app)
    app.add_middleware(RequestLoggingMiddleware)

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

    return app


if __name__ == "__main__":
    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=8000)
