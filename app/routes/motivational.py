from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.motivation import Motivation
from app.database import get_db
from typing import List
from app import MotivationResponse, MotivationCreate

router = APIRouter()

@router.post("/", response_model=MotivationResponse)
def create_motivation(motivation: MotivationCreate, db: Session = Depends(get_db)):
    new_motivation = Motivation(**motivation.dict())
    db.add(new_motivation)
    db.commit()
    db.refresh(new_motivation)
    return new_motivation


@router.get("/", response_model=List[MotivationResponse])
def get_all_motivations(db: Session = Depends(get_db)):
    return db.query(Motivation).all()
