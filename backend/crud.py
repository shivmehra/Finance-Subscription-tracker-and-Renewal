"""Database operations. Each function takes a Session and does one job.

Computed fields (days_until_renewal, is_urgent) are attached here when reading
so route handlers stay thin and the engine remains the single source of truth.
"""
from sqlalchemy.orm import Session

import engine
import models
import schemas


def _to_out(sub: models.Subscription) -> dict:
    """Serialize an ORM row and attach live-computed renewal fields."""
    days = engine.days_until_renewal(sub.renewal_date)
    return {
        "id": sub.id,
        "name": sub.name,
        "cost": sub.cost,
        "billing_cycle": sub.billing_cycle,
        "monthly_cost": sub.monthly_cost,
        "renewal_date": sub.renewal_date,
        "is_active": sub.is_active,
        "days_until_renewal": days,
        "is_urgent": engine.is_urgent(days),
    }


def create_sub(db: Session, payload: schemas.SubCreate) -> dict:
    monthly = engine.normalize_to_monthly(payload.cost, payload.billing_cycle)
    sub = models.Subscription(
        name=payload.name,
        cost=payload.cost,
        billing_cycle=payload.billing_cycle,
        monthly_cost=monthly,
        renewal_date=payload.renewal_date,
        is_active=True,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return _to_out(sub)


def get_all(db: Session) -> list[dict]:
    rows = (
        db.query(models.Subscription)
        .order_by(models.Subscription.id.desc())
        .all()
    )
    return [_to_out(s) for s in rows]


def get_metrics(db: Session) -> dict:
    rows = db.query(models.Subscription).all()
    return engine.compute_metrics(rows)


def toggle_active(db: Session, sub_id: int) -> dict | None:
    """Flip is_active without deleting. Returns None if not found."""
    sub = db.get(models.Subscription, sub_id)
    if sub is None:
        return None
    sub.is_active = not sub.is_active
    db.commit()
    db.refresh(sub)
    return _to_out(sub)


def delete_sub(db: Session, sub_id: int) -> bool:
    sub = db.get(models.Subscription, sub_id)
    if sub is None:
        return False
    db.delete(sub)
    db.commit()
    return True
