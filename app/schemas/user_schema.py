from pydantic import BaseModel, EmailStr, Field
from app.db.models.user import UserRole, UserStatus
from datetime import datetime
from uuid import UUID


class UserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=3, max_length=255)
    role: UserRole = Field(default=UserRole.CUSTOMER)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    created_at: datetime = Field(..., default_factory=datetime.now)


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    status: UserStatus
    created_at: datetime

    class Config:
        from_attributes = True
