from pydantic import BaseModel, Field, HttpUrl


class RecipeCandidate(BaseModel):
    title: str
    url: HttpUrl
    ingredients: list[str] = Field(default_factory=list)


class GroupedRecipe(BaseModel):
    title: str
    url: HttpUrl
    missing_ingredients: list[str] = Field(default_factory=list)


class RecipeSuggestionRequest(BaseModel):
    inventory: list[str] = Field(default_factory=list)
    pantry_staples: list[str] = Field(
        default_factory=lambda: ["salt", "pepper", "oil", "water", "butter"]
    )
    max_missing: int = Field(default=3, ge=0, le=3)
    limit: int = Field(default=10, ge=1, le=20)
    max_carbs: int | None = Field(default=None, ge=1)


class RecipeSuggestionResponse(BaseModel):
    can_make_now: list[GroupedRecipe] = Field(default_factory=list)
    missing_a_few: list[GroupedRecipe] = Field(default_factory=list)
