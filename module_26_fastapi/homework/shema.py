from pydantic import BaseModel, Field
from typing import List

class Recipe(BaseModel):
    name: str = Field(...,
        title="Recipe Name",
        description="Recipe Name",
        min_length=1,
        max_length=30,
    )
    time_rice: float = Field(...,
        title="Time Rice",
        description="Time Rice",
        ge=0.0,
    )
    ingredients: List[str] = Field(...,
        title="Ingredients",
        description="Ingredients",
    )
    text: str = Field(...,)

class RecipeResponse(BaseModel):
    id: int
    name: str
    time_rice: float
    ingredients: List[str]
    text: str

    class Config:
        orm_mode = True

class PeopleLook(BaseModel):
    name: str
    count_look: int
    time_rice: int

    class Config:
        orm_mode = True