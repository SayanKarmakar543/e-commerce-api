from fastapi import APIRouter
from app.db.session import db_dependency
from app.schemas.user_schema import UserRequest, UserResponse
from starlette import status
from app.core.settings import user_dependency
import uuid
from app.repositories.user_repository import (
    get_user_repository,
    get_user_by_id_repository,
    create_user_repository,
    update_user_repository,
    delete_user_repository
)

router = APIRouter(
    prefix="/api/v1",
    tags=["users"]
)


@router.get(
    "/users", 
    status_code=status.HTTP_200_OK
)
async def get_users(user: user_dependency, db: db_dependency):
    """
    Retrieve all users from the database.
    """
    return get_user_repository(user, db)


@router.get(
    "/users/{id}",
    status_code=status.HTTP_200_OK
)
async def get_user_by_id(
    user: user_dependency,
    db: db_dependency,
    user_id: uuid.UUID
):
    """
    Retrieve a user by their ID from the database.
    """
    return get_user_by_id_repository(user, db, user_id)


@router.post(
    "/users", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def create_user(
    user: user_dependency,
    db: db_dependency, 
    user_request: UserRequest,
):
    """
    Create a new user in the database.
    """
    return create_user_repository(user, db, user_request)


@router.put(
    "/users/{id}", 
    status_code=status.HTTP_200_OK, 
    response_model=UserResponse
)
async def update_user(
    user: user_dependency,
    db: db_dependency,
    id: uuid.UUID,
    user_request: UserRequest
):
    """
    Update an existing user in the database.
    """
    return update_user_repository(user, db, id, user_request)


@router.delete(
    "/user/{id}",
    status_code=status.HTTP_200_OK
)
async def delete_user(
    user: user_dependency,
    db: db_dependency,
    id: uuid.UUID
):
    
    """
    Delete a user from the database.
    """
    
    return delete_user_repository(user, db, id)
