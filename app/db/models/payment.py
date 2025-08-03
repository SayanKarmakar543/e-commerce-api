from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import uuid
import enum

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class PaymentMethod(enum.Enum):
    CARD = "card"
    UPI = "upi"
    COD = "cod"

class Payment(Base):

    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )
    amount = Column(String(20), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False, default=PaymentMethod.COD)
    created_at = Column(DateTime, server_default=func.now())
