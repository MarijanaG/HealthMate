from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


# User Schemas
class UserPreference(str, Enum):
    vegan = "vegan"
    vegetarian = "vegetarian"
    omnivorous = "omnivorous"


class UserType(str, Enum):
    nutritionist = "Nutritionist"
    client = "Client"


class UserBase(BaseModel):
    username: str
    age: int
    weight: float
    preference: UserPreference  # Using Enum for validation
    user_type: UserType  # Using Enum for validation

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True


# Recipe Schemas
class RecipeType(str, Enum):
    vegan = "vegan"
    vegetarian = "vegetarian"
    omnivorous = "omnivorous"


class RecipeBase(BaseModel):
    meal_plan_id: int
    name_recipe: str
    description: Optional[str] = None
    portion: float
    calories: int
    carbohydrates: float
    fats: float
    ingredients: List[str]  # List for multiple ingredients
    instructions: List[str]  # List for multiple instructions
    type: RecipeType

    class Config:
        from_attributes = True


class RecipeCreate(RecipeBase):
    pass


class RecipeResponse(RecipeBase):
    recipe_id: int

    class Config:
        from_attributes = True


# Meal Plan Schemas
class MealPlanBase(BaseModel):
    name: str
    description: str
    user_id: int

    class Config:
        from_attributes = True


class MealPlanCreate(BaseModel):
    name: str
    description: Optional[str] = None


class MealPlanResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class NutritionalType(str, Enum):
    vegan = "vegan"
    vegetarian = "vegetarian"
    omnivorous = "omnivorous"


# Base schema for nutritional plan
class NutritionalPlanBase(BaseModel):
    name: str
    description: str
    calories: float
    protein: float
    carbohydrates: float
    fats: float
    type: NutritionalType

    class Config:
        from_attributes = True


class NutritionalPlanCreate(NutritionalPlanBase):
    pass


class NutritionalPlanResponse(NutritionalPlanBase):
    id: int

    class Config:
        from_attributes = True


class MotivationBase(BaseModel):
    message: str

    class Config:
        from_attributes = True


class MotivationCreate(MotivationBase):
    pass


class MotivationResponse(MotivationBase):
    id: int

    class Config:
        from_attributes = True
