from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.models.nutritional_plan import NutritionalPlan
from app.schemas import NutritionalPlanCreate, NutritionalPlanResponse, NutritionalPlanUpdate
from app.database import get_db
from typing import List


router = APIRouter(
    prefix="/nutritional-plans",
    tags=["Nutritional Plans"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/{user_id}/{nutritionist}", response_model=NutritionalPlanResponse)
def create_nutritional_plan(user_id: int, nutritionist: int, nutritional_plan: NutritionalPlanCreate, db: Session = Depends(get_db)):
    new_nutritional_plan = NutritionalPlan(**nutritional_plan.dict())
    new_nutritional_plan.user_id=user_id
    new_nutritional_plan.nutritionist=nutritionist
    db.add(new_nutritional_plan)
    db.commit()
    db.refresh(new_nutritional_plan)
    return new_nutritional_plan


@router.get("/{user_id}/{nutritionist}", response_model=List[NutritionalPlanResponse])
def get_user_nutritional_plans(user_id: int, nutritionist: int, db: Session = Depends(get_db)):
    result = db.query(NutritionalPlan).filter(NutritionalPlan.user_id == user_id, NutritionalPlan.nutritionist == nutritionist)
    return result


@router.patch("/{user_id}", response_model=NutritionalPlanResponse)
def patch_nutritional_plan(user_id: int, updated_plan: NutritionalPlanUpdate, db: Session = Depends(get_db)):
    # Find the nutritional plan by ID
    nutritional_plan = db.query(NutritionalPlan).filter(NutritionalPlan.user_id == user_id).first()
    if not nutritional_plan:
        raise HTTPException(status_code=404, detail="Nutritional plan not found")

    # Update only the fields provided in the request
    update_data = updated_plan.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(nutritional_plan, key, value)

    db.commit()
    db.refresh(nutritional_plan)
    return nutritional_plan


@router.delete("/{user_id}", response_model=NutritionalPlanResponse)
def delete_nutritional_plan(user_id: int, db: Session = Depends(get_db)):
    nutritional_plan = db.query(NutritionalPlan).filter(NutritionalPlan.user_id == user_id).first()
    if not nutritional_plan:
        raise HTTPException(status_code=404, detail="Nutritional plan not found")

    db.delete(nutritional_plan)
    db.commit()
    return nutritional_plan