from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from urllib.parse import quote_plus
from app.config import settings


def build_database_url() -> str:
    # Prefer full DATABASE_URL if injected (Render Postgres, Railway, etc.)
    if settings.DATABASE_URL:
        url = settings.DATABASE_URL
        # Render injects postgres:// but SQLAlchemy needs postgresql://
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

    # Fall back to individual MySQL fields (local dev)
    return (
        f"mysql+pymysql://{settings.DB_USER}:{quote_plus(settings.DB_PASSWORD)}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


DATABASE_URL = build_database_url()

# Add pool_pre_ping so stale connections are detected and recycled (important for cloud DBs)
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
