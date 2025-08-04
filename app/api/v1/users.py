from fastapi import APIRouter
from app.db.session import db_dependency
from app.schemas.user_schema import UserRequest, UserResponse
from starlette import status
from app.repositories.user_repository import (
    get_user_repository,
    create_user_repository
)

router = APIRouter()

@router.get("/users", status_code=status.HTTP_200_OK)
def get_users(db: db_dependency):
    """
    Retrieve all users from the database.
    """
    return get_user_repository(db)

@router.post("/users", status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(
    db: db_dependency, 
    user_request: UserRequest,
):
    """
    Create a new user in the database.
    """
    return create_user_repository(db, user_request)
