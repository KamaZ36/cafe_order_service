from datetime import datetime

from pydantic import BaseModel

from zernyshko.domain.entities.order import OrderStatus


class CreatePickupOrderSchema(BaseModel):
    desired_time: datetime

    comment: str | None = None


class GetOrderListSchema(BaseModel):
    limit: int = 20
    offset: int = 0


class GetStaffOrderListSchema(BaseModel):
    limit: int = 50
    offset: int = 0
    status: OrderStatus | None = None


class StaffCancelOrderSchema(BaseModel):
    reason: str | None = None
