import os

from bus import make_consumer, make_publisher
from notifications_logic import NotificationHandler, ProcessedStore


def main():
    store = ProcessedStore(os.getenv("PROCESSED_DB", "/data/processed.db"))
    handler = NotificationHandler(store, make_publisher())
    consumer = make_consumer("notifications")
    print("notifications started", flush=True)
    for message in consumer:
        try:
            handler.handle(message.value)
        except Exception as error:
            print(f"failed to handle message: {error}", flush=True)


if __name__ == "__main__":
    main()
