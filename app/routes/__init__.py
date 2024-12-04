from .user_routes import router as user_router
from .recipe_routes import router as recipe_router
from app.database import get_db
from .meal_plan_routes import router as meal_plan_router
from .motivational import router as motivation_router
from .user_routes import router as user_router
from .nutritional_plan_routes import router as nutritional_plan_router

from app.schemas import UserCreate, UserResponse, RecipeCreate, RecipeResponse, MealPlanCreate, MealPlanResponse, MotivationCreate, MotivationResponse
