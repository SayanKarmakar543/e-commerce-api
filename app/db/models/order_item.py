from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.sql import func
import uuid

class OrderItem(Base):

    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
