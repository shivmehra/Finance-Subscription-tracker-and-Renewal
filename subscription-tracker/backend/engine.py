"""Core business logic — all financial computation lives here, server-side.

Two responsibilities:
  1. Cost Uniformity Engine  — normalize any billing cycle to a monthly rate.
  2. Date Intersect Calculator — days until renewal + urgency flag.

The metrics aggregator combines both over the ACTIVE subscriptions only, which
is what powers the real-time "pause = savings" simulation on the dashboard.
"""
from datetime import date

URGENT_WINDOW_DAYS = 7


def normalize_to_monthly(cost: float, billing_cycle: str) -> float:
    """Reduce any billing cycle to an equivalent monthly cost.

    A yearly subscription is divided across 12 months so it can be summed
    alongside monthly subscriptions on a common basis.
    """
    cycle = billing_cycle.strip().capitalize()
    if cycle == "Monthly":
        return round(cost, 2)
    if cycle == "Yearly":
        return round(cost / 12, 2)
    raise ValueError("billing_cycle must be 'Monthly' or 'Yearly'")


def days_until_renewal(renewal_date_str: str, today: date | None = None) -> int:
    """Whole days from today until the renewal date, floored at 0.

    `today` is injectable for testing; defaults to the server clock so the
    client can never spoof the reference date.
    """
    today = today or date.today()
    renewal = date.fromisoformat(renewal_date_str)
    return max((renewal - today).days, 0)


def is_urgent(days: int) -> bool:
    """A renewal is urgent when it falls within the next 7 days (inclusive)."""
    return days <= URGENT_WINDOW_DAYS


def compute_metrics(subscriptions) -> dict:
    """Aggregate the top-of-dashboard metrics over ACTIVE subscriptions only.

    Paused subscriptions are excluded from both the burn rate and the urgent
    count — this is the mechanism behind the savings simulation.
    """
    today = date.today()
    active = [s for s in subscriptions if s.is_active]
    burn = sum(s.monthly_cost for s in active)
    urgent = sum(
        1 for s in active if is_urgent(days_until_renewal(s.renewal_date, today))
    )
    return {"total_monthly_burn": round(burn, 2), "urgent_count": urgent}
