from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserResponse
from app.models.user import User
from app.database import SessionLocal
from typing import List
from app.utils import get_password_hash


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Depends(get_db)

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = db_dependency):
    existing_user = db.query(User).filter_by(e_mail=user.e_mail).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    user.password = get_password_hash(user.password)
    new_user = User(**user.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating user")



@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    try:
        return db.query(User).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching users")

