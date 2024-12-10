from datetime import date
from pydantic import BaseModel, EmailStr, Field
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
    full_name: Optional[str] = Field(None, example="John Doe")
    username: Optional[str] = Field(None, example="johndoe123")
    e_mail: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    age: Optional[int] = Field(None, example=30)
    weight: Optional[float] = Field(None, example=75.5)
    preference: Optional[UserPreference] = Field(None, example="vegan")
    user_type: Optional[UserType] = Field(None, example="Client")

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, example="John Doe")
    username: Optional[str] = Field(None, example="johndoe123")
    e_mail: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    age: Optional[int] = Field(None, example=30)
    weight: Optional[float] = Field(None, example=75.5)
    preference: Optional[UserPreference] = Field(None, example="vegan")
    user_type: Optional[UserType] = Field(None, example="Client")
    password: Optional[str] = Field(None, example="newpassword123")

    class Config:
        from_attributes = True

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

class RecipeUpdate(BaseModel):
    meal_plan_id: Optional[int] = None
    name_recipe: Optional[str] = None
    description: Optional[str] = None
    portion: Optional[float] = None
    calories: Optional[int] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    type: Optional[RecipeType] = None

    class Config:
        from_attributes = True


class RecipeResponse(RecipeBase):
    recipe_id: int

    class Config:
        from_attributes = True


# Meal Plan Schemas
class MealPlanBase(BaseModel):
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    class Config:
        from_attributes = True


class MealPlanCreate(MealPlanBase):
    plan_id: int  # Required for creation


class MealPlanUpdate(BaseModel):
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    plan_id: Optional[int] = None

    class Config:
        from_attributes = True


class MealPlanResponse(BaseModel):
    meal_plan_id: int
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]

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


class NutritionalPlanUpdate(BaseModel):
    calories: Optional[int] = None
    protein: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    type: Optional[NutritionalType] = None

    class Config:
        from_attributes = True


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
