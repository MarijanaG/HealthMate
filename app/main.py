import os
import sys
from datetime import datetime, timezone, timedelta
import uvicorn
from jose import jwt, JWTError
from enum import Enum
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from app.auth import get_current_user
from app.routes.user_routes import router as user_router
from app.routes.motivational import router as motivation_router
from app.routes.recipe_routes import router as recipe_router
from app.routes.meal_plan_routes import router as meal_plan_router
from app.routes.nutritional_plan_routes import router as nutritional_plan_router
from typing import Annotated
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_db, SessionLocal, initialize_database
from passlib.context import CryptContext
from app.schemas import Token
from app.utils import verify_password
from app.models import User


app = FastAPI()

# Include routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(nutritional_plan_router, prefix="/nutritional-plans", tags=["Nutritional Plans"])
app.include_router(meal_plan_router, prefix="/meal-plans", tags=["Meal Plans"])
app.include_router(recipe_router, prefix="/recipes", tags=["Recipes"])
app.include_router(motivation_router, prefix="/motivations", tags=["Motivations"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "m1a2r3i4j5a6n7a8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user


'''def decode_token(token: str, db: Session):
    user = get_user(db, token)
    return user'''


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


async def get_current_active_user(
        current_user: User = Depends(get_current_user),
):
    return current_user


@app.get("/users/me")
async def read_users_me(
        current_user: User = Depends(get_current_active_user),
):
    return current_user


'''@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user": user}'''


@app.get("/items/")
async def read_items(current_user: Annotated[User, Depends(get_current_user)]):
    return {"user": current_user}


@app.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[Session, Depends(get_db)]
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@app.get("/")
def read_root():
    return {"message": "Hello beautiful world"}


@app.get("/users/")
async def get_users(db: Annotated[Session, Depends(get_db)]):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")


#initialize_database()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
