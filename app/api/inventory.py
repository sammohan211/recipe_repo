from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db import get_session
from app.models.inventory import GroceryListItem, Ingredient, PantryStaple

router = APIRouter(prefix="/api", tags=["inventory"])


# --- Ingredients ---

class IngredientCreate(BaseModel):
    name: str


@router.get("/inventory", response_model=list[Ingredient])
def list_ingredients(session: Session = Depends(get_session)) -> list[Ingredient]:
    return list(session.exec(select(Ingredient)).all())


@router.post("/inventory", response_model=Ingredient, status_code=201)
def add_ingredient(body: IngredientCreate, session: Session = Depends(get_session)) -> Ingredient:
    existing = session.exec(select(Ingredient).where(Ingredient.name == body.name)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Ingredient already exists")
    ingredient = Ingredient(name=body.name.strip().lower())
    session.add(ingredient)
    session.commit()
    session.refresh(ingredient)
    return ingredient


@router.patch("/inventory/{ingredient_id}/toggle", response_model=Ingredient)
def toggle_ingredient(ingredient_id: int, session: Session = Depends(get_session)) -> Ingredient:
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    ingredient.present = not ingredient.present
    session.add(ingredient)
    session.commit()
    session.refresh(ingredient)
    return ingredient


@router.delete("/inventory/{ingredient_id}", status_code=204)
def remove_ingredient(ingredient_id: int, session: Session = Depends(get_session)) -> None:
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    session.delete(ingredient)
    session.commit()


# --- Pantry Staples ---

@router.get("/staples", response_model=list[PantryStaple])
def list_staples(session: Session = Depends(get_session)) -> list[PantryStaple]:
    return list(session.exec(select(PantryStaple)).all())


# --- Grocery List ---

class GroceryItemCreate(BaseModel):
    name: str


@router.get("/grocery", response_model=list[GroceryListItem])
def list_grocery(session: Session = Depends(get_session)) -> list[GroceryListItem]:
    return list(session.exec(select(GroceryListItem)).all())


@router.post("/grocery", response_model=GroceryListItem, status_code=201)
def add_grocery_item(body: GroceryItemCreate, session: Session = Depends(get_session)) -> GroceryListItem:
    item = GroceryListItem(name=body.name.strip())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.patch("/grocery/{item_id}/purchased", response_model=GroceryListItem)
def mark_purchased(item_id: int, session: Session = Depends(get_session)) -> GroceryListItem:
    item = session.get(GroceryListItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.purchased = not item.purchased
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/grocery/{item_id}", status_code=204)
def remove_grocery_item(item_id: int, session: Session = Depends(get_session)) -> None:
    item = session.get(GroceryListItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
