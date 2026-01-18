from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
import time

from app.api.events import router as events_router
from app.db.base import Base
from app.db.session import engine
import app.models  # register models

app = FastAPI(title="API Drift Detection Service")

@app.on_event("startup")
def startup_db():
    retries = 10
    delay = 2  # seconds

    for attempt in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database connected & tables created")
            break
        except OperationalError:
            print(f"⏳ DB not ready, retrying ({attempt + 1}/{retries})...")
            time.sleep(delay)
    else:
        raise RuntimeError("❌ Could not connect to database")

app.include_router(events_router, prefix="/api/v1")
