from app.models.recipes import (
    GroupedRecipe,
    RecipeCandidate,
    RecipeSuggestionRequest,
    RecipeSuggestionResponse,
)
from app.services.spoonacular_client import SpoonacularClient


class RecipeSuggester:
    def __init__(self, client: SpoonacularClient | None = None) -> None:
        self.client = client or SpoonacularClient()

    async def suggest(self, payload: RecipeSuggestionRequest) -> RecipeSuggestionResponse:
        raw_candidates = await self.client.find_recipes_by_ingredients(
            ingredients=payload.inventory,
            limit=payload.limit,
            max_carbs=payload.max_carbs,
        )

        candidates = [RecipeCandidate.model_validate(item) for item in raw_candidates]
        return group_recipes(
            candidates=candidates,
            inventory=payload.inventory,
            pantry_staples=payload.pantry_staples,
            max_missing=payload.max_missing,
        )


def _normalize(name: str) -> str:
    return name.strip().lower()


def group_recipes(
    candidates: list[RecipeCandidate],
    inventory: list[str],
    pantry_staples: list[str],
    max_missing: int,
) -> RecipeSuggestionResponse:
    present = {_normalize(i) for i in inventory if i.strip()}
    staples = {_normalize(i) for i in pantry_staples if i.strip()}

    can_make_now: list[GroupedRecipe] = []
    missing_a_few: list[GroupedRecipe] = []

    for candidate in candidates:
        missing = [
            _normalize(ingredient)
            for ingredient in candidate.ingredients
            if _normalize(ingredient)
            and _normalize(ingredient) not in present
            and _normalize(ingredient) not in staples
        ]

        unique_missing = sorted(set(missing))
        grouped = GroupedRecipe(
            title=candidate.title,
            url=candidate.url,
            missing_ingredients=unique_missing,
        )

        if not unique_missing:
            can_make_now.append(grouped)
        elif len(unique_missing) <= max_missing:
            missing_a_few.append(grouped)

    return RecipeSuggestionResponse(can_make_now=can_make_now, missing_a_few=missing_a_few)
