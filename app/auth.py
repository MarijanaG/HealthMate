from typing import Annotated
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from app.database import get_db
from app.dependencies import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.schemas import TokenData


'''def get_user():
    from app.main import get_user
    return get_user()'''


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

    from app.main import get_user

    user = get_user(db, username=username)
    if user is None:
        print("User not found in database")
        raise credentials_exception
    return user