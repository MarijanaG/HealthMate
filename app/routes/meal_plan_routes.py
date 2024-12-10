from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
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


@router.put("/{meal_plan_id}", response_model=MealPlanResponse)
def update_meal_plan(meal_plan_id: int, updated_meal_plan: MealPlanCreate, db: Session = Depends(get_db)):
    # Find the meal plan by ID
    meal_plan = db.query(MealPlan).filter(MealPlan.meal_plan_id == meal_plan_id).first()
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    # Update the meal plan fields with the new data
    for key, value in updated_meal_plan.dict().items():
        setattr(meal_plan, key, value)

    db.commit()
    db.refresh(meal_plan)
    return meal_plan


@router.delete("/{meal_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal_plan(meal_plan_id: int, db: Session = Depends(get_db)):
    # Find the meal plan by ID
    meal_plan = db.query(MealPlan).filter(MealPlan.meal_plan_id == meal_plan_id).first()
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    # Delete the meal plan
    db.delete(meal_plan)
    db.commit()
    return None
