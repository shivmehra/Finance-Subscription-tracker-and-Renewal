"""ORM models. A single Subscription table backs the entire dashboard."""
from sqlalchemy import Boolean, Column, Float, Integer, String

from database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # Raw cost exactly as the user entered it (per their chosen billing cycle).
    cost = Column(Float, nullable=False)
    billing_cycle = Column(String, nullable=False)  # "Monthly" | "Yearly"
    # Cost normalized to a monthly rate, computed once at insert time.
    monthly_cost = Column(Float, nullable=False)
    renewal_date = Column(String, nullable=False)  # ISO date string: YYYY-MM-DD
    is_active = Column(Boolean, nullable=False, default=True)
