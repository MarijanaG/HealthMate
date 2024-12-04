import os
import sys
from fastapi import FastAPI
from app.routes.motivational import router as motivation_router
from app.routes.user_routes import router as user_router
from app.routes.recipe_routes import router as recipe_router
from app.routes.meal_plan_routes import router as meal_plan_router
from app.routes.nutritional_plan_routes import router as nutritional_plan_router


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI()

# Include routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(recipe_router, prefix="/recipes", tags=["Recipes"])
app.include_router(meal_plan_router, prefix="/meal-plans", tags=["Meal Plans"])
app.include_router(motivation_router, prefix="/motivations", tags=["Motivations"])


@app.get("/")
def read_root():
    return {"message": "Hello beautiful world"}


# To run the app with `uvicorn app.main:app --reload`, this block is not necessary but is a good practice.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
