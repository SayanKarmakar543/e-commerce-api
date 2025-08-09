from fastapi import APIRouter
from app.db.session import db_dependency
from app.schemas.user_schema import UserRequest, UserResponse
from starlette import status
import uuid
from app.repositories.user_repository import (
    get_user_repository,
    create_user_repository,
    update_user_repository,
    delete_user_repository
)

router = APIRouter()


@router.get(
    "/users", 
    status_code=status.HTTP_200_OK
)
async def get_users(db: db_dependency):
    """
    Retrieve all users from the database.
    """
    return get_user_repository(db)


@router.post(
    "/users", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def create_user(
    db: db_dependency, 
    user_request: UserRequest,
):
    """
    Create a new user in the database.
    """
    return create_user_repository(db, user_request)


@router.put(
    "/users/{id}", 
    status_code=status.HTTP_200_OK, 
    response_model=UserResponse
)
async def update_user(
    db: db_dependency,
    id: uuid.UUID,
    user_request: UserRequest
):
    """
    Update an existing user in the database.
    """
    return update_user_repository(db, id, user_request)


@router.delete(
    "/user/{id}",
    status_code=status.HTTP_200_OK
)
async def delete_user(
    db: db_dependency,
    id: uuid.UUID
):
    
    """
    Delete a user from the database.
    """
    
    return delete_user_repository(db, id)
