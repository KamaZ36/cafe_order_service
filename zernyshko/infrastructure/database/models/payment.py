from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)

from zernyshko.domain.entities.payment import Payment, PaymentStatus
from zernyshko.infrastructure.database.models.base import mapper_registry

PAYMENT_TABLE = Table(
    "payments",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("provider_payment_id", String, nullable=True, unique=True),
    Column("user_id", UUID, ForeignKey("users.id"), nullable=False),
    Column("order_id", UUID, ForeignKey("orders.id"), nullable=False),
    Column("amount", Integer, nullable=False),
    Column("status", Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
)


mapper_registry.map_imperatively(
    Payment,
    PAYMENT_TABLE,
    properties={
        "_id": PAYMENT_TABLE.c.id,
        "_provider_payment_id": PAYMENT_TABLE.c.provider_payment_id,
        "_user_id": PAYMENT_TABLE.c.user_id,
        "_order_id": PAYMENT_TABLE.c.order_id,
        "_amount": PAYMENT_TABLE.c.amount,
        "_status": PAYMENT_TABLE.c.status,
        "_created_at": PAYMENT_TABLE.c.created_at,
        "_updated_at": PAYMENT_TABLE.c.updated_at,
    },
)
