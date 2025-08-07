from app.db.models.user import User  
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRequest
from fastapi import HTTPException
from fastapi import status


def get_user_repository(db: Session):

    users = db.query(User).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found."
        )

def create_user_repository(db: Session, user_request: UserRequest):

    # Check if the email already exists
    existing_email = db.query(User).filter(User.email==user_request.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists."
        )   

    create_user_model = User(
        name=user_request.name,
        email=user_request.email,
        password_hash=user_request.password,
        role=user_request.role,
        is_active=user_request.status,
        created_at=user_request.created_at
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

    return {
        "id": create_user_model.id,
        "name": create_user_model.name,
        "email": create_user_model.email,
        "role": create_user_model.role,
        "status": create_user_model.is_active,  # map to 'status'
        "created_at": create_user_model.created_at,
    }
