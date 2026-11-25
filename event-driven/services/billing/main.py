import os

from billing_logic import BillingHandler, ProcessedStore
from bus import make_consumer, make_publisher


def main():
    store = ProcessedStore(os.getenv("PROCESSED_DB", "/data/processed.db"))
    handler = BillingHandler(store, make_publisher())
    consumer = make_consumer("billing")
    print("billing started", flush=True)
    for message in consumer:
        try:
            handler.handle(message.value)
        except Exception as error:
            print(f"failed to handle message: {error}", flush=True)


if __name__ == "__main__":
    main()
