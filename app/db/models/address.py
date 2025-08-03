from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.sql import func
import uuid


class Address(Base):

    __tablename__ = "address"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
