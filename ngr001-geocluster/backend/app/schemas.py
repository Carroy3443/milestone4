"""
Pydantic Schemas Module

This module defines Pydantic models for request/response validation and
serialization in the NGR001 Geospatial API. These schemas ensure data
integrity and provide automatic API documentation.

Classes:
    EventIn: Schema for creating new events
    EventUpdate: Schema for updating existing events
    EventOut: Schema for event responses
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any


class EventIn(BaseModel):
    """
    Input schema for creating new geospatial events.
    
    Attributes:
        occurred_at: Timestamp when the event occurred
        lat: Latitude coordinate (WGS84, -90 to 90)
        lon: Longitude coordinate (WGS84, -180 to 180)
        type: Optional event type classification
        severity: Optional severity level (0-4 scale)
        properties: Additional metadata as key-value pairs
    """
    occurred_at: datetime
    lat: float
    lon: float
    type: Optional[str] = None
    severity: Optional[int] = None
    properties: dict[str, Any] = Field(default_factory=dict)


class EventUpdate(BaseModel):
    """
    Input schema for updating existing events.
    
    Only the id field is required; all other fields are optional
    and will only update if provided.
    
    Attributes:
        id: Event ID to update (required)
        type: New event type classification
        severity: New severity level
        occurred_at: New timestamp
    """
    id: int
    type: Optional[str] = None
    severity: Optional[str] = None
    occurred_at: Optional[datetime] = None


class EventOut(EventIn):
    """
    Output schema for event responses.
    
    Extends EventIn with the database-generated id field.
    Configured to work with SQLAlchemy ORM objects.
    
    Attributes:
        id: Unique identifier for the event
        (inherits all attributes from EventIn)
    """
    id: int

    class Config:
        """Pydantic configuration for ORM compatibility."""
        from_attributes = True
