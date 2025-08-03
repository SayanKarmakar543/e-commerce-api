from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
import uuid


class ProcuctReview(Base):

    __tablename__ = "product_reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    rating = Column(Integer, nullable=False) # 1-5 scale
    comment = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
