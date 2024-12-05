import os
import sys
from enum import Enum
from fastapi import FastAPI, Depends, HTTPException, status
from app.routes.motivational import router as motivation_router
from app.routes.user_routes import router as user_router
from app.routes.recipe_routes import router as recipe_router
from app.routes.meal_plan_routes import router as meal_plan_router
from app.routes.nutritional_plan_routes import router as nutritional_plan_router
from typing import Annotated
from pydantic import BaseModel
import jwt
from jwt import PyJWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

# Include routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(recipe_router, prefix="/recipes", tags=["Recipes"])
app.include_router(meal_plan_router, prefix="/meal-plans", tags=["Meal Plans"])
app.include_router(motivation_router, prefix="/motivations", tags=["Motivations"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "m1a2r3i4j5a6n7a8"
ALGORITHM = "HS256"


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "e_mail": "johndoe@example.com",
        "hashed_password": "hashedsecret",
        "disabled": False,
        "age": 30,
        "weight": 70.5,
        "preference": "omnivorous",
    }
}


class DietaryPreference(str, Enum):
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"
    OMNIVOROUS = "omnivorous"


def fake_hash_password(password: str) -> str:
    return "hashed" + password


class User(BaseModel):
    username: str
    full_name: str
    e_mail: str
    disabled: bool | None = None
    age: int
    weight: float
    preference: DietaryPreference


class UserInDB(User):
    hashed_password: str


def decode_token(token: str) -> UserInDB:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    print("hello")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    print("Hello")
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    print("python")
    return current_user


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user": user}


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/")
def read_root():
    return {"message": "Hello beautiful world"}


@app.get("/users/")
async def get_users():
    try:
        # Fetch all users from the database
        return fake_users_db
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching users")





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
