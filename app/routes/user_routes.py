from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserResponse
from app.models.user import User
from app.database import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash password before storing it
    user.password = hash_password(user.password)  # Make sure hash_password is imported from app.hashing
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

