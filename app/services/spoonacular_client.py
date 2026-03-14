import os
from typing import Any

import httpx

SPOONACULAR_BASE = "https://api.spoonacular.com"


class SpoonacularClient:
    async def find_recipes_by_ingredients(
        self,
        ingredients: list[str],
        limit: int,
        diet: str = "ketogenic",
        max_carbs: int | None = None,
    ) -> list[dict[str, Any]]:
        api_key = os.getenv("SPOONACULAR_API_KEY", "")
        if not api_key:
            raise RuntimeError("SPOONACULAR_API_KEY is not configured")

        params: dict[str, Any] = {
            "apiKey": api_key,
            "includeIngredients": ",".join(ingredients),
            "diet": diet,
            "number": limit,
            "fillIngredients": True,
            "addRecipeInformation": True,
            "sort": "max-used-ingredients",
        }
        if max_carbs is not None:
            params["maxCarbs"] = max_carbs

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                f"{SPOONACULAR_BASE}/recipes/complexSearch",
                params=params,
            )
            response.raise_for_status()
            data = response.json()

        return [
            {
                "title": r["title"],
                "url": r.get("sourceUrl", ""),
                "ingredients": [
                    i["name"]
                    for i in r.get("usedIngredients", []) + r.get("missedIngredients", [])
                ],
            }
            for r in data.get("results", [])
            if r.get("sourceUrl")
        ]
