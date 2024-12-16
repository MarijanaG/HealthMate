from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.models import MealPlan
from app.schemas import RecipeCreate, RecipeResponse, RecipeUpdate
from app.models.recipe import Recipe
from app.database import get_db
from typing import List


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/{meal_plan_id}", response_model=RecipeResponse)
def create_recipe(meal_plan_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    # Create a new recipe instance
    new_recipe = Recipe(**recipe.dict(), meal_plan_id = meal_plan_id)
    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe
    except Exception as e:
        print(f"Error creating recipe: {e}")
        db.rollback()  # Rollback if an error occurs during commit
        raise HTTPException(status_code=500, detail="Error creating recipe")


@router.get("/{meal_plan_id}", response_model=List[RecipeResponse])
def get_all_recipes(meal_plan_id: int, db: Session = Depends(get_db)):
    try:
        recipes = db.query(Recipe).filter(Recipe.meal_plan_id == meal_plan_id)

        if not recipes:
            raise HTTPException(status_code=404, detail="No recipes found for this meal plan")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching recipes")


@router.patch("/{meal_plan_id}/{recipe_id}", response_model=RecipeResponse)
def patch_recipe(meal_plan_id: int, recipe_id: int, updated_recipe: RecipeUpdate, db: Session = Depends(get_db)):
    # Query for the recipe based on meal_plan_id and recipe_id
    recipe = db.query(Recipe).filter(
        Recipe.recipe_id == recipe_id,
        Recipe.meal_plan_id == meal_plan_id
    ).first()

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found in the specified meal plan")

    # Update only fields provided in the request body
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
@router.delete("/{meal_plan_id}/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(meal_plan_id: int, recipe_id: int, db: Session = Depends(get_db)):
    # Query for the recipe based on meal_plan_id and recipe_id
    recipe = db.query(Recipe).filter(
        Recipe.recipe_id == recipe_id,
        Recipe.meal_plan_id == meal_plan_id
    ).first()

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found in the specified meal plan")

    try:
        db.delete(recipe)
        db.commit()
        return None  # Return 204 No Content
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting recipe")
