from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.models.meal_plan import MealPlan
from app.database import get_db
from typing import List
from app import MealPlanCreate, MealPlanResponse
from app.schemas import MealPlanUpdate

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


@router.patch("/{meal_plan_id}", response_model=MealPlanResponse)
def patch_meal_plan(meal_plan_id: int, updated_meal_plan: MealPlanUpdate, db: Session = Depends(get_db)):
    # Find the meal plan by ID
    meal_plan = db.query(MealPlan).filter(MealPlan.meal_plan_id == meal_plan_id).first()
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    # Update only the fields that are provided in the request body
    update_data = updated_meal_plan.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(meal_plan, key, value)

    try:
        db.commit()
        db.refresh(meal_plan)
        return meal_plan
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating meal plan")


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
