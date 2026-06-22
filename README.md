# Subscription Tracker & Renewal Dashboard

A personal finance dashboard that aggregates recurring SaaS and streaming
subscriptions, tracks renewal dates, and monitors monthly cash-flow burn.

All business logic — cost normalization, renewal-date math, and metric
aggregation — runs **server-side**. The frontend is presentation only.

---

## Features

- **Entry form** — service name, cost, billing cycle (Monthly / Yearly), and a
  calendar date-picker for the next renewal date.
- **Metrics row** — two live cards: **Total Monthly Burn Rate** and
  **Upcoming Renewals Alert Count** (renewals within 7 days).
- **Subscription grid** — every subscription in a table. Items renewing within
  7 days get an amber **"Renewing Soon"** badge.
- **Active / Paused toggle** — pausing a subscription **greys out the row but
  never deletes it**, and instantly removes its cost from the burn rate — a
  real-time savings simulation. Re-activating restores it.

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10 or later |
| pip | bundled with Python |
| Node.js | 18 or later |
| npm | bundled with Node.js |

Verify before running:

```bash
python --version   # Python 3.10+
node --version     # v18+
npm --version
```

---

## Quick start — single command

```bash
# 1. Clone the repo
git clone https://github.com/shivmehra/subscription-tracker.git
cd subscription-tracker

# 2. Launch (installs deps automatically on first run)
python start.py
```

`start.py` will:

1. Run `pip install -r backend/requirements.txt`
2. Run `npm install` inside `frontend/` (first run only — skipped if
   `node_modules/` already exists)
3. Start the FastAPI backend on **http://localhost:8000**
4. Start the Vite dev server on **http://localhost:5173**

Open **http://localhost:5173** in your browser. Press `Ctrl+C` in the terminal
to stop both servers.

---

## Project structure

```
subscription-tracker/
├── start.py              ← single-command launcher
├── .gitignore
├── README.md
│
├── backend/
│   ├── requirements.txt  ← fastapi uvicorn sqlalchemy pydantic
│   ├── main.py           ← FastAPI app (thin HTTP layer)
│   ├── database.py       ← SQLite engine + session factory
│   ├── models.py         ← ORM model (Subscription table)
│   ├── schemas.py        ← Pydantic request/response schemas
│   ├── engine.py         ← Cost Uniformity Engine + Date Intersect Calculator
│   └── crud.py           ← DB operations + computed-field serialization
│
└── frontend/
    ├── package.json
    ├── vite.config.js    ← proxies /api → http://localhost:8000
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx        ← state owner; re-fetches after every mutation
        ├── App.css        ← design tokens + all styles
        ├── api/
        │   └── client.js  ← thin fetch() wrappers, no state
        └── components/
            ├── MetricsRow.jsx
            ├── EntryForm.jsx
            ├── SubTable.jsx
            └── ToggleSwitch.jsx
```

---

## Architecture

### Backend (FastAPI + SQLite)

All computation lives in `backend/engine.py`:

**Cost Uniformity Engine** — normalizes every subscription to a monthly rate
so mixed billing cycles can be summed on one basis:

```
Monthly  →  cost as-is
Yearly   →  cost ÷ 12
```

**Date Intersect Calculator** — computes days until renewal against the
**server clock** (client can never spoof the reference date) and flags
anything within 7 days as urgent.

**Metrics aggregation** — burn rate and urgent count are computed over
**active subscriptions only**, which powers the pause/savings simulation.

### Frontend (React + Vite)

Pure presentation. `App.jsx` holds all state and re-fetches from the server
after every mutation so computed fields never drift from the backend.

---

## REST API

| Method | Path | Purpose |
|---|---|---|
| `POST`   | `/api/subscriptions` | Create; cost normalized server-side |
| `GET`    | `/api/subscriptions` | All subs + computed `days_until_renewal`, `is_urgent` |
| `GET`    | `/api/metrics` | `total_monthly_burn` + `urgent_count` (active only) |
| `PATCH`  | `/api/subscriptions/{id}/toggle` | Flip active/paused (never deletes) |
| `DELETE` | `/api/subscriptions/{id}` | Hard delete |

Interactive docs: **http://localhost:8000/docs**

---

## Notes

- Data is stored in `backend/subscriptions.db` (SQLite). This file is
  git-ignored so every clone starts with an empty database.
- The Vite dev server proxies `/api` requests to the backend — no CORS
  configuration needed in the browser.
- To run the servers manually (two separate terminals):
  ```bash
  # Terminal 1
  cd backend && python -m uvicorn main:app --reload

  # Terminal 2
  cd frontend && npm run dev
  ```
