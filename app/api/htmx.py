from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import Response
from sqlmodel import Session, select

from app.db import get_session
from app.models.inventory import GroceryListItem, Ingredient, PantryStaple
from app.models.recipes import RecipeCandidate
from app.services.recipe_suggester import group_recipes
from app.services.spoonacular_client import SpoonacularClient
from app.templates_config import templates

router = APIRouter(prefix="/htmx", tags=["htmx"])


# --- Inventory ---

@router.post("/inventory")
def add_ingredient_htmx(
    request: Request,
    name: str = Form(...),
    session: Session = Depends(get_session),
):
    clean = name.strip().lower()
    existing = session.exec(select(Ingredient).where(Ingredient.name == clean)).first()
    if not existing:
        ing = Ingredient(name=clean)
        session.add(ing)
        session.commit()
        session.refresh(ing)
    else:
        ing = existing
        if not ing.present:
            ing.present = True
            session.add(ing)
            session.commit()
    return templates.TemplateResponse(
        "partials/ingredient_item.html", {"request": request, "ing": ing}
    )


@router.patch("/inventory/{ingredient_id}/toggle")
def toggle_ingredient_htmx(
    ingredient_id: int, request: Request, session: Session = Depends(get_session)
):
    ing = session.get(Ingredient, ingredient_id)
    if not ing:
        return Response(status_code=404)
    ing.present = not ing.present
    session.add(ing)
    session.commit()
    session.refresh(ing)
    return templates.TemplateResponse(
        "partials/ingredient_item.html", {"request": request, "ing": ing}
    )


@router.delete("/inventory/{ingredient_id}")
def delete_ingredient_htmx(ingredient_id: int, session: Session = Depends(get_session)):
    ing = session.get(Ingredient, ingredient_id)
    if ing:
        session.delete(ing)
        session.commit()
    return Response(content="", status_code=200)


# --- Grocery ---

@router.post("/grocery")
def add_grocery_htmx(
    request: Request,
    name: str = Form(...),
    session: Session = Depends(get_session),
):
    item = GroceryListItem(name=name.strip())
    session.add(item)
    session.commit()
    session.refresh(item)
    return templates.TemplateResponse(
        "partials/grocery_item.html", {"request": request, "item": item}
    )


@router.patch("/grocery/{item_id}/purchased")
def toggle_purchased_htmx(
    item_id: int, request: Request, session: Session = Depends(get_session)
):
    item = session.get(GroceryListItem, item_id)
    if not item:
        return Response(status_code=404)
    item.purchased = not item.purchased
    session.add(item)
    session.commit()
    session.refresh(item)
    return templates.TemplateResponse(
        "partials/grocery_item.html", {"request": request, "item": item}
    )


@router.delete("/grocery/{item_id}")
def delete_grocery_htmx(item_id: int, session: Session = Depends(get_session)):
    item = session.get(GroceryListItem, item_id)
    if item:
        session.delete(item)
        session.commit()
    return Response(content="", status_code=200)


# --- Recipes ---

@router.post("/recipes")
async def suggest_recipes_htmx(request: Request, session: Session = Depends(get_session)):
    ingredients = [
        i.name for i in session.exec(select(Ingredient).where(Ingredient.present == True)).all()
    ]
    staples = [s.name for s in session.exec(select(PantryStaple)).all()]
    search_query = "keto recipes with " + " ".join(ingredients[:6])

    if not ingredients:
        return templates.TemplateResponse(
            "partials/recipe_results.html",
            {"request": request, "error": "No ingredients in pantry.", "can_make_now": [],
             "missing_a_few": [], "search_query": "keto recipes"},
        )

    try:
        client = SpoonacularClient()
        raw = await client.find_recipes_by_ingredients(ingredients=ingredients, limit=10)
        candidates = [RecipeCandidate.model_validate(r) for r in raw]
        result = group_recipes(
            candidates=candidates,
            inventory=ingredients,
            pantry_staples=staples,
            max_missing=3,
        )
    except RuntimeError as exc:
        return templates.TemplateResponse(
            "partials/recipe_results.html",
            {"request": request, "error": str(exc), "can_make_now": [],
             "missing_a_few": [], "search_query": search_query},
        )

    return templates.TemplateResponse(
        "partials/recipe_results.html",
        {"request": request, "error": None, "can_make_now": result.can_make_now,
         "missing_a_few": result.missing_a_few, "search_query": search_query},
    )
