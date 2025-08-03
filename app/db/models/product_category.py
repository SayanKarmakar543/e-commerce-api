from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey
import uuid

class ProductCategory(Base):

    __tablename__ = "product_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("product_categories.id", ondelete="SET NULL"),
        nullable=True
    )
