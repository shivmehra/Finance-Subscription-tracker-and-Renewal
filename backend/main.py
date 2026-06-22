"""FastAPI application — HTTP layer only.

Route handlers validate input, delegate all logic to crud/engine, and shape
responses. No business logic lives here.
"""
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, engine, get_db

# Auto-create the SQLite schema on startup (zero-config first run).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Subscription Tracker API", version="1.0.0")

# Vite dev server origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/subscriptions", response_model=list[schemas.SubOut])
def list_subscriptions(db: Session = Depends(get_db)):
    return crud.get_all(db)


@app.post("/api/subscriptions", response_model=schemas.SubOut, status_code=201)
def create_subscription(payload: schemas.SubCreate, db: Session = Depends(get_db)):
    return crud.create_sub(db, payload)


@app.get("/api/metrics", response_model=schemas.MetricsOut)
def get_metrics(db: Session = Depends(get_db)):
    return crud.get_metrics(db)


@app.patch("/api/subscriptions/{sub_id}/toggle", response_model=schemas.SubOut)
def toggle_subscription(sub_id: int, db: Session = Depends(get_db)):
    result = crud.toggle_active(db, sub_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return result


@app.delete("/api/subscriptions/{sub_id}", status_code=204)
def delete_subscription(sub_id: int, db: Session = Depends(get_db)):
    if not crud.delete_sub(db, sub_id):
        raise HTTPException(status_code=404, detail="Subscription not found")
    return None
