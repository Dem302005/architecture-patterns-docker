import sqlite3
from datetime import datetime, timezone

PRICES = {1: 100.0, 2: 49.9, 3: 15.5}
DEFAULT_PRICE = 10.0


def now_iso():
    return datetime.now(timezone.utc).isoformat()


class ProcessedStore:
    def __init__(self, path=":memory:"):
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute("CREATE TABLE IF NOT EXISTS processed_event_ids (id TEXT PRIMARY KEY)")
        self._conn.commit()

    def seen(self, key):
        row = self._conn.execute("SELECT 1 FROM processed_event_ids WHERE id = ?", (key,)).fetchone()
        return row is not None

    def mark(self, key):
        self._conn.execute("INSERT OR IGNORE INTO processed_event_ids (id) VALUES (?)", (key,))
        self._conn.commit()


class BillingHandler:
    def __init__(self, store, publish):
        self._store = store
        self._publish = publish

    def handle(self, event):
        if event.get("eventType") != "OrderCreated":
            return None
        order_id = event["orderId"]
        if self._store.seen(order_id):
            print(f"duplicate OrderCreated ignored orderId={order_id}", flush=True)
            return None
        amount = round(PRICES.get(event["itemId"], DEFAULT_PRICE) * event["qty"], 2)
        payment = {"eventType": "PaymentCaptured", "orderId": order_id, "amount": amount, "ts": now_iso()}
        self._publish(payment)
        self._store.mark(order_id)
        print(f"payment captured orderId={order_id} amount={amount}", flush=True)
        return payment
