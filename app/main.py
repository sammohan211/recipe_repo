from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.htmx import router as htmx_router
from app.api.inventory import router as inventory_router
from app.api.pages import router as pages_router
from app.api.recipes import router as recipes_router
from app.api.scan import router as scan_router
from app.db import create_db_and_tables, seed_pantry_staples

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    create_db_and_tables()
    seed_pantry_staples()
    yield


app = FastAPI(title="Pantry Inventory & Recipe Assistant", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages_router)
app.include_router(htmx_router)
app.include_router(inventory_router)
app.include_router(recipes_router)
app.include_router(scan_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
