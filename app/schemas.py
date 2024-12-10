from datetime import date
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
    full_name: str
    username: str
    e_mail: str
    age: int
    weight: float
    preference: UserPreference
    user_type: UserType


class UserCreate(UserBase):
    password: str


class UserResponse(BaseModel):
    user_id: int
    full_name: str
    username: str
    e_mail: str
    age: int
    weight: float
    preference: UserPreference
    user_type: UserType

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
    description: str
    start_date: date
    end_date: date

    class Config:
        from_attributes = True


class MealPlanCreate(BaseModel):
    description: Optional[str] = None
    start_date: date
    end_date: date
    plan_id: int


class MealPlanResponse(BaseModel):
    meal_plan_id: int

    class Config:
        from_attributes = True


class NutritionalType(str, Enum):
    vegan = "vegan"
    vegetarian = "vegetarian"
    omnivorous = "omnivorous"


# Base schema for nutritional plan
class NutritionalPlanBase(BaseModel):
    calories: int
    protein: float
    carbohydrates: float
    fats: float
    type: NutritionalType

    class Config:
        from_attributes = True


class NutritionalPlanCreate(NutritionalPlanBase):
    pass


class NutritionalPlanResponse(NutritionalPlanBase):
    plan_id: int

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
