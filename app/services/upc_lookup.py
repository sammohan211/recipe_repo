import os

import httpx

OFF_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
UPCITEMDB_URL = "https://api.upcitemdb.com/prod/trial/lookup"

USER_AGENT = os.getenv("APP_USER_AGENT", "PantryAssistant/1.0")


async def _lookup_open_food_facts(barcode: str) -> str | None:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            OFF_URL.format(barcode=barcode),
            headers={"User-Agent": USER_AGENT},
        )
    if response.status_code != 200:
        return None
    data = response.json()
    if data.get("status") != 1:
        return None
    product = data.get("product", {})
    name = product.get("product_name") or product.get("product_name_en")
    return name.strip() if name else None


async def _lookup_upcitemdb(barcode: str) -> str | None:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(UPCITEMDB_URL, params={"upc": barcode})
    if response.status_code != 200:
        return None
    items = response.json().get("items", [])
    if not items:
        return None
    title = items[0].get("title")
    return title.strip() if title else None


async def lookup_upc(barcode: str) -> str | None:
    """Open Food Facts first, UPCitemdb as fallback. Returns None if both miss."""
    name = await _lookup_open_food_facts(barcode)
    if name:
        return name
    return await _lookup_upcitemdb(barcode)
