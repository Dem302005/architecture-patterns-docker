import sqlite3
from datetime import datetime, timezone


def now_iso():
    return datetime.now(timezone.utc).isoformat()


class ProcessedStore:
    def __init__(self, path=":memory:"):
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute("CREATE TABLE IF NOT EXISTS processed_event_ids (id TEXT PRIMARY KEY)")
        self._conn.commit()

    def seen(self, key):
        return self._conn.execute("SELECT 1 FROM processed_event_ids WHERE id = ?", (key,)).fetchone() is not None

    def mark(self, key):
        self._conn.execute("INSERT OR IGNORE INTO processed_event_ids (id) VALUES (?)", (key,))
        self._conn.commit()


class NotificationHandler:
    def __init__(self, store, publish):
        self._store = store
        self._publish = publish

    def handle(self, event):
        if event.get("eventType") != "PaymentCaptured":
            return None
        order_id = event["orderId"]
        if self._store.seen(order_id):
            print(f"duplicate PaymentCaptured ignored orderId={order_id}", flush=True)
            return None
        recipient = f"order-{order_id}@example.com"
        print(f"EMAIL to={recipient} text='Payment {event['amount']} received'", flush=True)
        sent = {"eventType": "EmailSent", "orderId": order_id, "to": recipient, "ts": now_iso()}
        self._publish(sent)
        self._store.mark(order_id)
        return sent
