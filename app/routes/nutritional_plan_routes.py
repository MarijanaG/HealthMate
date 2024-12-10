from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.nutritional_plan import NutritionalPlan
from app.schemas import NutritionalPlanCreate, NutritionalPlanResponse, NutritionalPlanUpdate
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


@router.patch("/{plan_id}", response_model=NutritionalPlanResponse)
def patch_nutritional_plan(plan_id: int, updated_plan: NutritionalPlanUpdate, db: Session = Depends(get_db)):
    # Find the nutritional plan by ID
    nutritional_plan = db.query(NutritionalPlan).filter(NutritionalPlan.plan_id == plan_id).first()
    if not nutritional_plan:
        raise HTTPException(status_code=404, detail="Nutritional plan not found")

    # Update only the fields provided in the request
    update_data = updated_plan.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(nutritional_plan, key, value)

    db.commit()
    db.refresh(nutritional_plan)
    return nutritional_plan


@router.delete("/{plan_id}", response_model=NutritionalPlanResponse)
def delete_nutritional_plan(plan_id: int, db: Session = Depends(get_db)):
    nutritional_plan = db.query(NutritionalPlan).filter(NutritionalPlan.plan_id == plan_id).first()
    if not nutritional_plan:
        raise HTTPException(status_code=404, detail="Nutritional plan not found")

    db.delete(nutritional_plan)
    db.commit()
    return nutritional_plan