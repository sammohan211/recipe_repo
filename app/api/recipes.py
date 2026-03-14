from fastapi import APIRouter, HTTPException

from app.models.recipes import RecipeSuggestionRequest, RecipeSuggestionResponse
from app.services.recipe_suggester import RecipeSuggester

router = APIRouter(prefix="/api/recipes", tags=["recipes"])
suggester = RecipeSuggester()


@router.post("/suggest", response_model=RecipeSuggestionResponse)
async def suggest_recipes(payload: RecipeSuggestionRequest) -> RecipeSuggestionResponse:
    try:
        return await suggester.suggest(payload)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
