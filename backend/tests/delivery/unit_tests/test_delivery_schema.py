import pytest
from pydantic import ValidationError

from backend.schemas.delivery_schema import (
    DeliverySchema,
    DeliveryStatus,
    DeliveryStatusUpdateSchema,
)


def test_delivery_schema_valid_data():
    delivery = DeliverySchema(
        delivery_id=1,
        order_id=101,
        status=DeliveryStatus.PENDING,
        estimated_arrival="20 minutes",
        driver_name="Alex",
        driver_contact="555-1234",
    )

    assert delivery.delivery_id == 1
    assert delivery.order_id == 101
    assert delivery.status == DeliveryStatus.PENDING
    assert delivery.estimated_arrival == "20 minutes"
    assert delivery.driver_name == "Alex"
    assert delivery.driver_contact == "555-1234"


def test_delivery_schema_allows_optional_fields_to_be_none():
    delivery = DeliverySchema(
        delivery_id=2,
        order_id=102,
        status=DeliveryStatus.ASSIGNED,
    )

    assert delivery.estimated_arrival is None
    assert delivery.driver_name is None
    assert delivery.driver_contact is None


def test_delivery_schema_rejects_non_positive_delivery_id():
    with pytest.raises(ValidationError):
        DeliverySchema(
            delivery_id=0,
            order_id=101,
            status=DeliveryStatus.PENDING,
        )


def test_delivery_schema_rejects_non_positive_order_id():
    with pytest.raises(ValidationError):
        DeliverySchema(
            delivery_id=1,
            order_id=-10,
            status=DeliveryStatus.PENDING,
        )


def test_delivery_schema_rejects_blank_driver_name():
    with pytest.raises(ValidationError):
        DeliverySchema(
            delivery_id=1,
            order_id=101,
            status=DeliveryStatus.PENDING,
            driver_name="   ",
        )


def test_delivery_schema_rejects_blank_driver_contact():
    with pytest.raises(ValidationError):
        DeliverySchema(
            delivery_id=1,
            order_id=101,
            status=DeliveryStatus.PENDING,
            driver_contact="   ",
        )


def test_delivery_status_update_schema_valid():
    update = DeliveryStatusUpdateSchema(
        status=DeliveryStatus.ON_THE_WAY,
        estimated_arrival="10 minutes",
    )

    assert update.status == DeliveryStatus.ON_THE_WAY
    assert update.estimated_arrival == "10 minutes"


def test_delivery_status_update_schema_rejects_blank_eta():
    with pytest.raises(ValidationError):
        DeliveryStatusUpdateSchema(
            status=DeliveryStatus.PICKED_UP,
            estimated_arrival="   ",
        )