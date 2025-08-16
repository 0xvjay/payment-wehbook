from datetime import datetime

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db import PaymentEvent, SessionLocal
from app.utils import generate_signature_from_body, verify_signature

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/webhook/payments")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")
    if not signature or not verify_signature(signature, body.decode()):
        return JSONResponse(
            status_code=403,
            content={"message": "Invalid signature"},
        )

    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid JSON body"},
        )

    events = []
    if not isinstance(payload, list):
        payload = [payload]

    for event in payload:
        event_id = event.get("id")
        event_type = event.get("event")
        payment_id = event["payload"]["payment"]["entity"]["id"]

        if not all([event_id, event_type, payment_id]):
            return JSONResponse(
                status_code=400,
                content={"message": "Missing required fields"},
            )

        event_id = event_id.lower()

        if db.query(PaymentEvent).filter_by(event_id=event_id).first():
            return JSONResponse(
                status_code=200,
                content={"message": "Duplicate event"},
            )

        event_obj = PaymentEvent(
            event_id=event_id,
            payment_id=payment_id,
            event_type=event_type,
            received_at=datetime.utcnow(),
            payload=event,
        )
        events.append(event_obj)
    db.add_all(events)
    db.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "Event stored successfully"},
    )


@app.get("/payments/{payment_id}/events")
def get_payment_events(payment_id: str, db: Session = Depends(get_db)):
    events = (
        db.query(PaymentEvent)
        .filter_by(payment_id=payment_id)
        .order_by(PaymentEvent.received_at)
        .all()
    )

    if not events:
        return JSONResponse(
            status_code=404,
            content={"message": "No events found for this payment_id"},
        )

    return JSONResponse(
        status_code=200,
        content={
            "message": "Events retrieved successfully",
            "data": [
                {"event_type": e.event_type, "received_at": e.received_at.isoformat()}
                for e in events
            ],
        },
    )


@app.post("/generate-signature")
async def generate_sig(request: Request):
    body = await request.body()

    if not body:
        return JSONResponse(
            status_code=400,
            content={"message": "Empty request body"},
        )

    try:
        sig = generate_signature_from_body(body.decode("utf-8"))
        return JSONResponse(
            status_code=200,
            content={
                "message": "Signature generated successfully",
                "data": {"signature": sig},
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "message": f"Failed to generate signature: {str(e)}",
            },
        )
