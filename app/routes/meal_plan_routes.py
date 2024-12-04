from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.meal_plan import MealPlan
from app.database import get_db
from typing import List
from app import MealPlanCreate, MealPlanResponse


router = APIRouter()

@router.post("/", response_model=MealPlanResponse)
def create_meal_plan(meal_plan: MealPlanCreate, db: Session = Depends(get_db)):
    new_meal_plan = MealPlan(**meal_plan.dict())
    db.add(new_meal_plan)
    db.commit()
    db.refresh(new_meal_plan)
    return new_meal_plan

@router.get("/", response_model=List[MealPlanResponse])
def get_all_meal_plans(db: Session = Depends(get_db)):
    return db.query(MealPlan).all()
