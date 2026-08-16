from fastapi import FastAPI, status, Depends, HTTPException
from typing import List
from shema import Recipe, RecipeResponse, PeopleLook
from crud import get_session, create_recipe, crud_get_recipe, crud_get_recipes
from config import AsyncSession

app = FastAPI()


@app.post('/recipes', status_code=status.HTTP_201_CREATED, response_model=RecipeResponse)
async def created_recipes(recipe: Recipe, db: AsyncSession = Depends(get_session)):
    """
        Создать новый рецепт.
        - **name**: название (1–30 символов)
        - **time_rice**: время в минутах (≥0)
        - **ingredients**: список ингредиентов
        - **text**: описание
    """
    result = await create_recipe(db, recipe)
    return result


@app.get('/recipes/{id}', response_model=RecipeResponse, status_code=status.HTTP_200_OK)
async def get_recipe(id: int, db: AsyncSession = Depends(get_session)):
    result = await crud_get_recipe(db, id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return result


@app.get('/recipes', response_model=List[PeopleLook], status_code=status.HTTP_200_OK)
async def get_recipes(db: AsyncSession = Depends(get_session)):
    result = await crud_get_recipes(db)
    new_result = [
        PeopleLook(
            name=recipe.name,
            count_look=recipe.count_look,
            time_rice=recipe.time_rice,
        )
        for recipe in result
    ]
    return new_result
