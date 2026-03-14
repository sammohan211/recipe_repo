from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.db import get_session
from app.models.inventory import GroceryListItem, Ingredient, Product
from app.templates_config import templates

router = APIRouter(tags=["pages"])


@router.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/inventory", status_code=302)


@router.get("/inventory")
def inventory_page(request: Request, session: Session = Depends(get_session)):
    ingredients = list(session.exec(select(Ingredient)).all())
    return templates.TemplateResponse(
        "inventory.html", {"request": request, "active": "inventory", "ingredients": ingredients}
    )


@router.get("/scan")
def scan_page(request: Request):
    return templates.TemplateResponse(
        "scan.html", {"request": request, "active": "scan"}
    )


@router.get("/recipes")
def recipes_page(request: Request):
    return templates.TemplateResponse(
        "recipes.html", {"request": request, "active": "recipes"}
    )


@router.get("/grocery")
def grocery_page(request: Request, session: Session = Depends(get_session)):
    items = list(session.exec(select(GroceryListItem)).all())
    return templates.TemplateResponse(
        "grocery.html", {"request": request, "active": "grocery", "items": items}
    )


@router.post("/forms/scan/confirm")
def confirm_scan_form(
    upc: str = Form(...),
    product_name: str = Form(...),
    ingredient_name: str = Form(...),
    session: Session = Depends(get_session),
) -> RedirectResponse:
    # Upsert product cache
    product = session.get(Product, upc)
    if product:
        product.product_name = product_name
    else:
        product = Product(upc=upc, product_name=product_name)
    session.add(product)

    # Add or re-enable ingredient
    name = ingredient_name.strip().lower()
    ingredient = session.exec(select(Ingredient).where(Ingredient.name == name)).first()
    if not ingredient:
        session.add(Ingredient(name=name))
    elif not ingredient.present:
        ingredient.present = True
        session.add(ingredient)

    session.commit()
    return RedirectResponse(url="/inventory", status_code=303)
