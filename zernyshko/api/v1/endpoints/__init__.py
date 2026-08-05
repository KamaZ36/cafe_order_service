from .category import router as category_router
from .order import router as order_router
from .product import router as product_router
from .user import router as user_router

__all__ = ["category_router", "order_router", "product_router", "user_router"]
