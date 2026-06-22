# Subscription Tracker & Renewal Dashboard

A personal finance dashboard that aggregates recurring SaaS and streaming
subscriptions, tracks renewal dates, and monitors monthly cash-flow burn.

All business logic — cost normalization, renewal-date math, and metric
aggregation — runs **server-side**. The frontend is presentation only.

## Features

- **Entry form** — service name, cost, billing cycle (Monthly/Yearly), and a
  calendar date-picker for the next renewal date.
- **Metrics row** — two live cards: **Total Monthly Burn Rate** and
  **Upcoming Renewals Alert Count** (renewals within 7 days).
- **Subscription grid** — a table of every subscription. Items renewing within
  7 days get an amber **"Renewing Soon"** badge.
- **Active / Paused toggle** — pausing a subscription **greys out the row but
  never deletes it**, and instantly removes its cost from the burn rate — a
  real-time savings simulation. Re-activating restores it.

## Architecture

```
backend/   FastAPI + SQLAlchemy + SQLite        (all logic & state)
  engine.py    Cost Uniformity Engine + Date Intersect Calculator
  crud.py      DB operations + computed-field serialization
  main.py      REST API (thin HTTP layer)

frontend/  React + Vite                          (presentation only)
  src/api/client.js    thin fetch() wrappers
  src/App.jsx          state owner; refetches after every mutation
  src/components/      MetricsRow, EntryForm, SubTable, ToggleSwitch
```

### Core logic (`backend/engine.py`)

- **Cost Uniformity Engine** — normalizes every subscription to a monthly
  rate (`yearly / 12`) so mixed billing cycles can be summed on one basis.
- **Date Intersect Calculator** — computes days until renewal against the
  **server clock** and flags anything within 7 days as urgent.
- **Metrics** — burn rate and urgent count are aggregated over **active
  subscriptions only**, which is what powers the pause/savings simulation.

## Running locally

Requires Python 3.10+ and Node 18+.

**Terminal 1 — backend** (http://localhost:8000):
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

**Terminal 2 — frontend** (http://localhost:5173):
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server proxies `/api` to the backend.

## API

| Method | Path | Purpose |
|---|---|---|
| POST   | `/api/subscriptions` | Create; cost normalized server-side |
| GET    | `/api/subscriptions` | All subs + computed `days_until_renewal`, `is_urgent` |
| GET    | `/api/metrics` | `total_monthly_burn` + `urgent_count` (active only) |
| PATCH  | `/api/subscriptions/{id}/toggle` | Flip active/paused (no delete) |
| DELETE | `/api/subscriptions/{id}` | Remove a subscription |

Interactive API docs: http://localhost:8000/docs
