from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine, select

DATABASE_URL = "sqlite:///pantry.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

DEFAULT_STAPLES = ["salt", "pepper", "oil", "water", "butter"]


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def seed_pantry_staples() -> None:
    from app.models.inventory import PantryStaple

    with Session(engine) as session:
        existing = session.exec(select(PantryStaple)).all()
        if not existing:
            for name in DEFAULT_STAPLES:
                session.add(PantryStaple(name=name))
            session.commit()
