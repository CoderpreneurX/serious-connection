from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# Base class for models
Base = declarative_base()

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    future=True,
    pool_pre_ping=True,
    echo=settings.DEBUG,  # log SQL in dev
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


# Dependency for FastAPI
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
