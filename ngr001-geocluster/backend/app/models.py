"""
Database Models Module

This module defines SQLAlchemy ORM models for the NGR001 Geospatial Event
Clustering System. It provides the data model for storing geospatial events
with temporal and spatial attributes.

Classes:
    Base: SQLAlchemy declarative base class
    Event: Geospatial event model with location and metadata
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, JSON, Float
from datetime import datetime  # Python type (IMPORTANT)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base class for all models."""
    pass


class Event(Base):
    """
    Geospatial event model representing a single occurrence at a location.
    
    This model stores events with geographic coordinates, temporal information,
    and optional metadata. The database table includes a PostGIS geography
    column (geom) that is automatically generated from lat/lon coordinates.
    
    Attributes:
        id: Unique identifier for the event
        occurred_at: Timestamp when the event occurred
        lat: Latitude coordinate (WGS84)
        lon: Longitude coordinate (WGS84)
        type: Optional event type classification
        severity: Optional severity level (0-4 scale)
        properties: JSON object for additional metadata (e.g., source dataset)
    """
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    type: Mapped[str | None] = mapped_column(String, nullable=True)
    severity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    properties: Mapped[dict] = mapped_column(JSON, default=dict)
