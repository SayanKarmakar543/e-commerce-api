from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
from fastapi import HTTPException, status
from app.db.session import db_dependency
from app.db.models.user import User
from sqlalchemy.orm import Session
from app.repositories.user_repository import bcrypt_context
import uuid

SECRET_KEY = "b83c8709a46332d3bd34f126ac591ec508fbc2cd07b4a08795d3b3a7c142f875"
ALGORITHM = "HS256"


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def authenticate_user(username: str, password: str, db: Session):
    """Authenticate a user using username and password"""

    user = db.query(User).filter(User.name == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user


def create_access_token(username: str, user_id: uuid.UUID, role: str, expires_delta: timedelta):
    encode = {
        "sub": username,
        "id": str(user_id),
        "role": role.value if hasattr(role, "value") else role
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: uuid = payload.get("id")
        role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials."
            )
        return {"username": username, "id": user_id, "role": role}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials."
        )


user_dependency = Annotated[dict, Depends(get_current_user)]
