"""
Database Connection Module

This module manages database connections for the NGR001 Geospatial API.
It configures SQLAlchemy engine and session management for PostgreSQL/PostGIS.

The DATABASE_URL environment variable must be set to a valid PostgreSQL
connection string (e.g., postgresql+psycopg2://user:pass@host:port/dbname).

Functions:
    get_db: FastAPI dependency that yields database sessions
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
"""Database connection URL from environment variable."""

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
"""SQLAlchemy engine with connection pool health checks enabled."""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Session factory for creating database sessions."""


def get_db():
    """
    FastAPI dependency that provides database sessions.
    
    This generator function creates a new database session for each request
    and ensures proper cleanup after the request completes.
    
    Yields:
        Session: SQLAlchemy database session
    
    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
