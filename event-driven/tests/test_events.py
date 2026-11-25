import json
import pathlib

import pytest
from jsonschema import Draft7Validator

from billing_logic import BillingHandler
from billing_logic import ProcessedStore as BillingStore
from notifications_logic import NotificationHandler
from notifications_logic import ProcessedStore as NotificationStore
from orders_logic import OrderService, ValidationError

SCHEMAS = pathlib.Path(__file__).resolve().parent.parent / "schemas"


def validator(name):
    schema = json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))
    Draft7Validator.check_schema(schema)
    return Draft7Validator(schema)


class FakeBus:
    def __init__(self):
        self.log = []
        self.handlers = []

    def publish(self, event):
        self.log.append(event)
        for handler in list(self.handlers):
            handler.handle(event)

    def of_type(self, event_type):
        return [e for e in self.log if e["eventType"] == event_type]


@pytest.fixture
def system():
    bus = FakeBus()
    orders = OrderService(bus.publish)
    billing = BillingHandler(BillingStore(), bus.publish)
    notifications = NotificationHandler(NotificationStore(), bus.publish)
    bus.handlers = [billing, notifications]
    return bus, orders


def test_full_event_chain(system):
    bus, orders = system
    order_id = orders.create({"userId": 1, "itemId": 2, "qty": 2})
    assert [e["eventType"] for e in bus.log] == ["OrderCreated", "PaymentCaptured", "EmailSent"]
    assert all(e["orderId"] == order_id for e in bus.log)
    assert bus.of_type("PaymentCaptured")[0]["amount"] == 99.8


def test_all_events_match_json_schemas(system):
    bus, orders = system
    orders.create({"userId": 1, "itemId": 1, "qty": 1})
    for event in bus.log:
        errors = list(validator(event["eventType"]).iter_errors(event))
        assert not errors, (event, errors)


def test_republished_order_created_does_not_duplicate_payment(system):
    bus, orders = system
    order_id = orders.create({"userId": 1, "itemId": 1, "qty": 1})
    assert orders.republish(order_id)
    assert orders.republish(order_id)
    assert len(bus.of_type("OrderCreated")) == 3
    assert len(bus.of_type("PaymentCaptured")) == 1
    assert len(bus.of_type("EmailSent")) == 1


def test_duplicate_payment_event_does_not_send_second_email():
    published = []
    handler = NotificationHandler(NotificationStore(), published.append)
    event = {"eventType": "PaymentCaptured", "orderId": "o1", "amount": 5.0, "ts": "2026-01-01T00:00:00+00:00"}
    handler.handle(event)
    handler.handle(event)
    assert len(published) == 1


def test_different_orders_are_processed_independently(system):
    bus, orders = system
    orders.create({"userId": 1, "itemId": 1, "qty": 1})
    orders.create({"userId": 2, "itemId": 3, "qty": 2})
    assert len(bus.of_type("PaymentCaptured")) == 2


def test_processed_ids_survive_restart(tmp_path):
    path = str(tmp_path / "processed.db")
    published = []
    event = {"eventType": "OrderCreated", "orderId": "o1", "userId": 1, "itemId": 1, "qty": 1, "ts": "2026-01-01T00:00:00+00:00"}
    BillingHandler(BillingStore(path), published.append).handle(event)
    BillingHandler(BillingStore(path), published.append).handle(event)
    assert len(published) == 1


def test_billing_ignores_other_event_types():
    published = []
    BillingHandler(BillingStore(), published.append).handle({"eventType": "EmailSent", "orderId": "x"})
    assert published == []


@pytest.mark.parametrize("payload", [None, {}, {"userId": 1, "itemId": 1}, {"userId": 1, "itemId": 1, "qty": 0}, {"userId": "1", "itemId": 1, "qty": 1}])
def test_invalid_order_is_rejected_and_nothing_published(payload):
    published = []
    with pytest.raises(ValidationError):
        OrderService(published.append).create(payload)
    assert published == []


def test_order_created_schema_rejects_bad_event():
    bad = {"eventType": "OrderCreated", "orderId": "", "userId": 1, "itemId": 1, "qty": 0, "ts": "x"}
    assert list(validator("OrderCreated").iter_errors(bad))
