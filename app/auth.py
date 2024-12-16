from typing import Annotated
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from app.dependencies import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.schemas import TokenData
from app.utils import verify_password
from passlib.context import CryptContext
from app.database import get_db
from datetime import datetime, timezone, timedelta
from app.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "m1a2r3i4j5a6n7a8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Annotated[Session, Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(f"Decoded username: {username}")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        print("JWT decoding failed")
        raise credentials_exception


    user = get_user(db, username=username)
    if user is None:
        print("User not found in database")
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user),
):
    return current_user