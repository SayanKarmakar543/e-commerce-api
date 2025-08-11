from app.db.models.user import User  
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRequest
from fastapi import HTTPException, status
from app.db.models.user import UserRole
from passlib.context import CryptContext
import uuid


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_repository(user:dict, db: Session):

    if not user or UserRole(user.get("role")) != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to access this resource."
        )

    users_model = db.query(User).all()

    if not users_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found."
        )

    return users_model


def get_user_by_id_repository(user: dict, db: Session, user_id: uuid.UUID):

    if not user or UserRole(user.get("role")) != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to access this resource."
        )
    
    user_model = db.query(User).filter(User.id==user_id).first()

    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    return user_model


def create_user_repository(user: dict, db: Session, user_request: UserRequest):

    if not user or UserRole(user.get("role")) != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to access this resource."
        )

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
        password_hash=bcrypt_context.hash(user_request.password),
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
        "password": create_user_model.password_hash,  # Note: Password should not be returned in production
        "role": create_user_model.role,
        "status": create_user_model.is_active,  # map to 'status'
        "created_at": create_user_model.created_at,
    }


def update_user_repository(user: dict, db: Session, user_id: uuid, user_request: UserRequest):

    if not user or UserRole(user.get("role")) != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to access this resource."
        )

    user_model = db.query(User).filter(User.id==user_id).first()

    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    # Check if the email already exists for another user
    existing_email = db.query(User).filter(
        User.email==user_request.email, 
        User.id!=user_id
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists."
        )
    
    user_model.name = user_request.name
    user_model.email = user_request.email
    # user_model.password_hash = user_request.password
    # user_model.role = user_request.role
    # user_model.is_active = user_request.status
    user_model.created_at = user_request.created_at

    db.add(user_model)
    db.commit()
    
    return {
        "id": user_model.id,
        "name": user_model.name,
        "email": user_model.email,
        "role": user_model.role,
        "status": user_model.is_active,
        "created_at": user_model.created_at,
    }


def delete_user_repository(user: dict, db: Session, user_id: uuid):

    if not user or UserRole(user.get("role")) != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to access this resource."
        )

    user_model = db.query(User).filter(User.id==user_id).first()

    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    db.delete(user_model)
    db.commit()


def user_registration_repository(db: Session, user_request: UserRequest):

    if not user_request.email or not user_request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required."
        )
    
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
        password_hash=bcrypt_context.hash(user_request.password),
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
        "status": create_user_model.is_active,
        "created_at": create_user_model.created_at,
    }


def get_user_profile_repository(user: dict, db: Session):

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )
    
    user_model = db.query(User).filter(User.id==user.get("id")).first()

    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    return user_model


def update_user_profile_repository(user: dict, db: Session, user_request: UserRequest):

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )
    
    user_model = db.query(User).filter(User.id==user.get("id")).first()

    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    # Check if the email already exists for another user
    existing_email = db.query(User).filter(
        User.email==user_request.email, 
        User.id!=user_model.id
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists."
        )
    
    user_model.name = user_request.name
    user_model.email = user_request.email
    user_model.created_at = user_request.created_at

    db.add(user_model)
    db.commit()

    return {
        "id": user_model.id,
        "name": user_model.name,
        "email": user_model.email,
        "role": user_model.role,
        "status": user_model.is_active,
        "created_at": user_model.created_at,
    }
