import json
import os
import time

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

TOPIC = "orders.events"


def wait_for(factory):
    for _ in range(60):
        try:
            return factory()
        except NoBrokersAvailable:
            time.sleep(2)
    raise RuntimeError("Kafka is not available")


def make_publisher():
    servers = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
    producer = wait_for(
        lambda: KafkaProducer(
            bootstrap_servers=servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8"),
            acks="all",
            retries=5,
        )
    )

    def publish(event):
        producer.send(TOPIC, key=event["orderId"], value=event).get(timeout=10)
        print(f"published {event['eventType']} orderId={event['orderId']}", flush=True)

    return publish


def make_consumer(group_id):
    servers = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
    return wait_for(
        lambda: KafkaConsumer(
            TOPIC,
            bootstrap_servers=servers,
            group_id=group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda b: json.loads(b.decode("utf-8")),
        )
    )
