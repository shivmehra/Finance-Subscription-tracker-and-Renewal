"""Pydantic request/response schemas — the API contract.

Input is validated on the way in (SubCreate); computed fields are attached
on the way out (SubOut) so the frontend never has to recalculate anything.
"""
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class SubCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    cost: float = Field(..., gt=0)
    billing_cycle: Literal["Monthly", "Yearly"]
    renewal_date: str  # ISO date string YYYY-MM-DD

    @field_validator("renewal_date")
    @classmethod
    def _valid_iso_date(cls, v: str) -> str:
        # Raises ValueError -> 422 if the date string is malformed.
        date.fromisoformat(v)
        return v

    @field_validator("name")
    @classmethod
    def _strip_name(cls, v: str) -> str:
        return v.strip()


class SubOut(BaseModel):
    id: int
    name: str
    cost: float
    billing_cycle: str
    monthly_cost: float
    renewal_date: str
    is_active: bool
    # Computed live on every read, never persisted:
    days_until_renewal: int
    is_urgent: bool


class MetricsOut(BaseModel):
    total_monthly_burn: float
    urgent_count: int
