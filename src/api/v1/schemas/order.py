from datetime import datetime

from pydantic import BaseModel


class CreatePickupOrderSchema(BaseModel):
    desired_time: datetime

    comment: str | None = None
