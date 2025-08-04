from app.db.models.user import User  
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRequest


def get_user_repository(db: Session):

    return db.query(User).all()

def create_user_repository(db: Session, user_request: UserRequest):

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
