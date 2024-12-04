from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import RecipeCreate, RecipeResponse
from app.models.recipe import Recipe
from app.database import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    # Create a new recipe instance
    new_recipe = Recipe(**recipe.dict())
    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe
    except Exception as e:
        db.rollback()  # Rollback if an error occurs during commit
        raise HTTPException(status_code=500, detail="Error creating recipe")

@router.get("/", response_model=List[RecipeResponse])
def get_all_recipes(db: Session = Depends(get_db)):
    try:
        return db.query(Recipe).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching recipes")

