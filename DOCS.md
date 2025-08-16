# Project Documentation

## Data Model

### PaymentEvent (db.py)

| Field       | Type     | Description                                         |
| ----------- | -------- | --------------------------------------------------- |
| event_id    | String   | Unique identifier for the event (stored lowercase). |
| payment_id  | String   | Razorpay payment ID.                                |
| event_type  | String   | Type of event (e.g. `payment.authorized`).          |
| received_at | DateTime | UTC timestamp when the event was stored.            |
| payload     | JSON     | Full JSON payload as received from Razorpay.        |

---

## API Endpoints

### POST `/webhook/payments`

Receives webhook events and stores them after verifying signature.

**Headers**

- `Content-Type: application/json`
- `X-Razorpay-Signature: <calculated-signature>`

**Request Body**  
A single event object or an array of event objects.

**Responses**

- `200 OK`
  ```
  {"message": "Event stored successfully"}
  ```
  or
  ```
  {"message": "Duplicate event"}
  ```
- `400 Bad Request`
  ```
  {"message": "Missing required fields"}
  ```
- `403 Forbidden`
  ```
  {"message": "Invalid signature"}
  ```

---

### GET `/payments/{payment_id}/events`

Fetches all stored events for the given payment ID.

**Responses**

- `200 OK`
  ```
  {
    "message": "Events retrieved successfully",
    "data": [
      {"event_type": "payment.authorized", "received_at": "2025-08-16T12:34:56"}
    ]
  }
  ```
- `404 Not Found`
  ```
  {"message": "No events found for this payment_id"}
  ```

---

### POST `/generate-signature`

Generates a valid Razorpay signature for testing purposes.  
Signs the raw JSON body exactly as it would be sent by Razorpay.

**Responses**

- `200 OK`
  ```
  {
    "message": "Signature generated successfully",
    "data": {"signature": "A6hi79NRLXuo3S/..."}
  }
  ```
- `400 Bad Request`
  ```
  {"message": "Empty request body"}
  ```
