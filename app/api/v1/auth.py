from fastapi import APIRouter, Depends, HTTPException
from app.db.session import db_dependency
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from datetime import timedelta
from app.core.settings import authenticate_user, create_access_token
from app.schemas.user_schema import UserRequest
from app.core.settings import user_dependency
from app.repositories.user_repository import (
    user_registration_repository,
    get_user_profile_repository,
    update_user_profile_repository
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency 
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user."
        )
    
    token = create_access_token(user.name, user.id, user.role, timedelta(minutes=30))

    return {
        "message": "Login successful!",
        "access_token": token,
        "id": str(user.id),
        "role": user.role,
        "token_type": "bearer"
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_registration(
    db: db_dependency,
    user_request: UserRequest,
):
    """
    Register a new user in the system.
    """
    if not user_request.email or not user_request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required."
        )
    
    return user_registration_repository(db, user_request)


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_profile(
    user: user_dependency,
    db: db_dependency
):
    """
    Retrieve the profile of the currently authenticated user.
    """
    
    return get_user_profile_repository(user, db)


@router.put("/updateMe", status_code=status.HTTP_200_OK)
async def update_user_profile(
    user: user_dependency,
    db: db_dependency,
    user_request: UserRequest
):
    """
    Update the profile of the currently authenticated user.
    """
    
    return update_user_profile_repository(user, db, user_request)
