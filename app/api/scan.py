from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db import get_session
from app.models.inventory import Ingredient, Product
from app.services.upc_lookup import lookup_upc

router = APIRouter(prefix="/api/scan", tags=["scan"])


class ScanResponse(BaseModel):
    upc: str
    product_name: str | None
    from_cache: bool


class ConfirmRequest(BaseModel):
    upc: str
    product_name: str
    ingredient_name: str


@router.post("", response_model=ScanResponse)
async def scan_barcode(upc: str, session: Session = Depends(get_session)) -> ScanResponse:
    """Look up a UPC. Checks local cache first, then OFF, then UPCitemdb."""
    cached = session.get(Product, upc)
    if cached:
        return ScanResponse(upc=upc, product_name=cached.product_name, from_cache=True)

    product_name = await lookup_upc(upc)

    if product_name:
        session.add(Product(upc=upc, product_name=product_name))
        session.commit()

    return ScanResponse(upc=upc, product_name=product_name, from_cache=False)


@router.post("/confirm", response_model=Ingredient, status_code=201)
def confirm_scan(body: ConfirmRequest, session: Session = Depends(get_session)) -> Ingredient:
    """Save UPC→product name mapping and add ingredient to inventory."""
    # Upsert product cache entry
    product = session.get(Product, body.upc)
    if product:
        product.product_name = body.product_name
    else:
        product = Product(upc=body.upc, product_name=body.product_name)
    session.add(product)

    # Add ingredient if not already present
    name = body.ingredient_name.strip().lower()
    ingredient = session.exec(select(Ingredient).where(Ingredient.name == name)).first()
    if not ingredient:
        ingredient = Ingredient(name=name)
        session.add(ingredient)
    elif not ingredient.present:
        ingredient.present = True
        session.add(ingredient)
    else:
        raise HTTPException(status_code=409, detail="Ingredient already in inventory")

    session.commit()
    session.refresh(ingredient)
    return ingredient
