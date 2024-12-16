from datetime import timedelta
from typing import Annotated
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from app.auth import get_current_active_user, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    authenticate_user
from app.database import get_db, SessionLocal, initialize_database
from app.schemas import Token
from app.models import User
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/users/me")
async def read_users_me(
        current_user: User = Depends(get_current_active_user),
):
    return current_user


@router.get("/items/")
async def read_items(current_user: Annotated[User, Depends(get_current_user)]):
    return {"user": current_user}


@router.post("/token", response_model=Token)
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


'''@router.get("/")
def read_root():
    return {"message": "Hello beautiful world"}'''

@router.get("/")
async def root_redirect():
    return RedirectResponse(url="/docs")


@router.get("/users/")
async def get_users(db: Annotated[Session, Depends(get_db)]):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
