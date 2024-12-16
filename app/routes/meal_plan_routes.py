from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.auth import get_current_user
from app.models import Recipe
from app.models.nutritional_plan import NutritionalPlan
from app.models.meal_plan import MealPlan
from app.database import get_db
from typing import List
from app import MealPlanCreate, MealPlanResponse
from app.schemas import MealPlanUpdate
from sqlalchemy import and_


router = APIRouter(
    prefix="/meal-plans",
    tags=["Meal Plans"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/{{plan_id}", response_model=MealPlanResponse)
def create_meal_plan(plan_id: int, meal_plan: MealPlanCreate, db: Session = Depends(get_db)):
    new_meal_plan = MealPlan(**meal_plan.dict(), plan_id=plan_id)
    db.add(new_meal_plan)
    db.commit()
    db.refresh(new_meal_plan)
    return new_meal_plan


@router.get("/{user_id}/{plan_id}", response_model=List[MealPlanResponse])
def get_user_meal_plans(plan_id: int, user_id: int, db: Session = Depends(get_db)):
    result = db.query(MealPlan).filter(and_(MealPlan.plan_id == plan_id), (NutritionalPlan.user_id == user_id))
    return result

'''@router.get("/", response_model=List[MealPlanResponse])
def get_all_meal_plans(db: Session = Depends(get_db)):
    return db.query(MealPlan).all()'''


@router.patch("/{user_id}/{plan_id}", response_model=MealPlanResponse)
def patch_meal_plan(user_id: int,plan_id: int, updated_meal_plan: MealPlanUpdate, db: Session = Depends(get_db)):
    # Find the meal plan by ID
    meal_plan = (
        db.query(MealPlan)
        .join(NutritionalPlan, NutritionalPlan.plan_id == MealPlan.plan_id)
        .filter(MealPlan.plan_id == plan_id, NutritionalPlan.user_id == user_id)
        .first()
    )
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


@router.delete("/{user_id}/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal_plan(user_id: int, plan_id: int, db: Session = Depends(get_db)):
    # Find the meal plan by ID
    meal_plan = (
        db.query(MealPlan)
        .join(NutritionalPlan, NutritionalPlan.plan_id == MealPlan.plan_id)
        .filter(MealPlan.plan_id == plan_id, NutritionalPlan.user_id == user_id)
        .first()
    )

    if not meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    db.query(Recipe).filter(Recipe.meal_plan_id == plan_id).delete()

    # Delete the meal plan
    db.delete(meal_plan)
    db.commit()
    return None
