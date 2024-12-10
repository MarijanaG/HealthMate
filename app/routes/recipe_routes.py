from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import RecipeCreate, RecipeResponse, RecipeUpdate
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
        print(f"Error creating recipe: {e}")
        db.rollback()  # Rollback if an error occurs during commit
        raise HTTPException(status_code=500, detail="Error creating recipe")


@router.get("/", response_model=List[RecipeResponse])
def get_all_recipes(db: Session = Depends(get_db)):
    try:
        return db.query(Recipe).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching recipes")


@router.patch("/{recipe_id}", response_model=RecipeResponse)
def patch_recipe(recipe_id: int, updated_recipe: RecipeUpdate, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Only update fields provided in the request body
    update_data = updated_recipe.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(recipe, key, value)

    try:
        db.commit()
        db.refresh(recipe)
        return recipe
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating recipe")


# Delete a recipe by ID
@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    try:
        db.delete(recipe)
        db.commit()
        return None  # Return a 204 No Content status
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting recipe")
