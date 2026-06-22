"""SQLAlchemy engine, session factory, and declarative base.

A single SQLite file (subscriptions.db) lives alongside this module so the
app is zero-config: the file is auto-created on first startup.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./subscriptions.db"

# check_same_thread=False is required for SQLite under FastAPI's threaded server.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a request-scoped DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
