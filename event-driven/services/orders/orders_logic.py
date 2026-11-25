import uuid
from datetime import datetime, timezone

TOPIC = "orders.events"


class ValidationError(Exception):
    pass


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def is_positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


class OrderService:
    def __init__(self, publish):
        self._publish = publish
        self._events = {}

    def create(self, payload):
        if not isinstance(payload, dict):
            raise ValidationError("body must be a JSON object")
        for field in ("userId", "itemId", "qty"):
            if not is_positive_int(payload.get(field)):
                raise ValidationError(f"{field} must be a positive integer")
        event = {
            "eventType": "OrderCreated",
            "orderId": str(uuid.uuid4()),
            "userId": payload["userId"],
            "itemId": payload["itemId"],
            "qty": payload["qty"],
            "ts": now_iso(),
        }
        self._events[event["orderId"]] = event
        self._publish(event)
        return event["orderId"]

    def republish(self, order_id):
        event = self._events.get(order_id)
        if event is None:
            return False
        self._publish(dict(event))
        return True
