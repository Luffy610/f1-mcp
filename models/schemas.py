"""Pydantic schemas for MCP tool request and response models."""

from pydantic import BaseModel
from typing import List, Optional


class SessionRequest(BaseModel):
    """Request parameters identifying a specific F1 session."""
    year: int
    grand_prix: str
    session: str


class SeasonList(BaseModel):
    """Response containing a list of available F1 seasons."""
    seasons: List[int]


class GrandPrixList(BaseModel):
    """Response containing a list of Grand Prix names for a season."""
    races: List[str]