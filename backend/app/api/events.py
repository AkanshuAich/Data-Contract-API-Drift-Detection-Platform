from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.event import APIEventCreate
from app.models.api_event import APIEvent
from app.db.session import SessionLocal
from app.services.contract_inference import infer_structure
from app.models.api_contract import APIContract


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/events")
def ingest_event(event: APIEventCreate, db: Session = Depends(get_db)):
    db_event = APIEvent(**event.dict())
    db.add(db_event)
    db.commit()

    # Infer contract from response
    inferred_contract = infer_structure(event.response_body)

    # Get latest contract version
    latest = db.query(APIContract)\
        .filter_by(
            service=event.service,
            endpoint=event.endpoint,
            method=event.method
        )\
        .order_by(APIContract.version.desc())\
        .first()

    next_version = 1 if not latest else latest.version + 1

    contract = APIContract(
        service=event.service,
        endpoint=event.endpoint,
        method=event.method,
        version=next_version,
        contract=inferred_contract
    )

    db.add(contract)
    db.commit()

    return {
        "event_id": str(db_event.id),
        "contract_version": next_version,
        "status": "stored"
    }

