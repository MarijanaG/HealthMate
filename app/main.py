import uvicorn
from fastapi.openapi import docs
from jose import jwt, JWTError
from enum import Enum
from fastapi import FastAPI, Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from starlette.responses import RedirectResponse
from app.auth import get_current_user
from app.routes.user_routes import router as user_router
from app.routes.motivational import router as motivation_router
from app.routes.recipe_routes import router as recipe_router
from app.routes.meal_plan_routes import router as meal_plan_router
from app.routes.nutritional_plan_routes import router as nutritional_plan_router
from app.routes.auth_routes import router as auth_router


app = FastAPI()


# Include routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(nutritional_plan_router, prefix="/nutritional-plans", tags=["Nutritional Plans"])
app.include_router(meal_plan_router, prefix="/meal-plans", tags=["Meal Plans"])
app.include_router(recipe_router, prefix="/recipes", tags=["Recipes"])
app.include_router(motivation_router, prefix="/motivations", tags=["Motivations"])
app.include_router(auth_router, tags=["Auth"])


#initialize_database()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
