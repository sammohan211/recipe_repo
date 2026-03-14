from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    upc: str = Field(primary_key=True)
    product_name: str
    last_modified: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    present: bool = Field(default=True)


class PantryStaple(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)


class GroceryListItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    purchased: bool = Field(default=False)
