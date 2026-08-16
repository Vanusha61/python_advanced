from typing import List

from sqlalchemy import select

from config import async_session, AsyncSession
from shema import Recipe
from model import Dish


async def get_session():
    async with async_session() as session:
        yield session


async def create_recipe(db: AsyncSession, recipes: Recipe) -> Dish:
    try:
        dish = Dish(
            name=recipes.name,
            time_rice=recipes.time_rice,
            ingredients=recipes.ingredients,
            text=recipes.text
        )
        db.add(dish)
        await db.commit()
        await db.refresh(dish)
        return dish
    except Exception as e:
        await db.rollback()
        print(e)

async def crud_get_recipe(db: AsyncSession, id: int) -> Dish | None:
    try:
        dish = await db.execute(select(Dish).where(Dish.id == id))
        dish = dish.scalar_one_or_none()
        if dish is None:
            return None
        dish.add_view()
        await db.commit()
        await db.refresh(dish)
        return dish
    except Exception as e:
        await db.rollback()
        return None

async def crud_get_recipes(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Dish]:
    try:
        recipes = await db.execute(select(Dish).offset(skip).limit(limit).order_by(Dish.count_look.desc(), Dish.time_rice.asc()))
        recipes = recipes.scalars().all()
        return recipes
    except Exception as e:
        print(e)
        return []