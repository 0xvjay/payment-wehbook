# Razorpay Webhook Handler

## Project Structure

```
.
├── app/
│   ├── db.py       # Database setup and PaymentEvent model
│   ├── main.py     # FastAPI application and API endpoints
│   ├── utils.py    # Signature generation and verification
├── payments.db     # SQLite database (created automatically)
```

---

## Installation

Install dependencies:

```
pip install fastapi uvicorn sqlalchemy
```

---

## Running the Server

```
uvicorn app.main:app --reload
```

API documentation is available at:

```
http://localhost:8000/docs
```

---

## Example Usage

### Generate Signature

```
curl -X POST http://localhost:8000/generate-signature \
  -H "Content-Type: application/json" \
  -d @mock_payloads/payment_authorized.json
```

### Send Webhook Event

```
curl -X POST http://localhost:8000/webhook/payments \
  -H "Content-Type: application/json" \
  -H "X-Razorpay-Signature: <signature>" \
  -d @mock_payloads/payment_authorized.json
```

### Retrieve Events

```
curl http://localhost:8000/payments/pay_123/events
```

---

## Configuration

Set the webhook secret in `utils.py`:

```
SECRET = "your_webhook_secret"
```

Replace with the actual secret from Razorpay dashboard.
