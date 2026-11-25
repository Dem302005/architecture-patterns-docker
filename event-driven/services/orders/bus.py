import json
import os
import time

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from orders_logic import TOPIC


def make_publisher():
    servers = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
    producer = None
    for _ in range(60):
        try:
            producer = KafkaProducer(
                bootstrap_servers=servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8"),
                acks="all",
                retries=5,
            )
            break
        except NoBrokersAvailable:
            time.sleep(2)
    if producer is None:
        raise RuntimeError("Kafka is not available")

    def publish(event):
        producer.send(TOPIC, key=event["orderId"], value=event).get(timeout=10)
        print(f"published {event['eventType']} orderId={event['orderId']}", flush=True)

    return publish
