from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.nutritional_plan import NutritionalPlan
from app.schemas import NutritionalPlanCreate, NutritionalPlanResponse
from app.database import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=NutritionalPlanResponse)
def create_nutritional_plan(nutritional_plan: NutritionalPlanCreate, db: Session = Depends(get_db)):
    new_nutritional_plan = NutritionalPlan(**nutritional_plan.dict())
    db.add(new_nutritional_plan)
    db.commit()
    db.refresh(new_nutritional_plan)
    return new_nutritional_plan

@router.get("/", response_model=List[NutritionalPlanResponse])
def get_all_nutritional_plans(db: Session = Depends(get_db)):
    return db.query(NutritionalPlan).all()
