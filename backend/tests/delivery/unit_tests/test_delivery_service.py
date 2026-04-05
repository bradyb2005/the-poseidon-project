import pytest

from backend.schemas.delivery_schema import (
    DeliverySchema,
    DeliveryStatus,
    DeliveryStatusUpdateSchema,
)
from backend.services.delivery_service import DeliveryService


@pytest.fixture
def service():
    return DeliveryService()


@pytest.fixture
def sample_delivery():
    return DeliverySchema(
        delivery_id=1,
        order_id=101,
        status=DeliveryStatus.PENDING,
        estimated_arrival="25 minutes",
    )


def test_create_delivery(service, sample_delivery):
    created_delivery = service.create_delivery(sample_delivery)

    assert created_delivery.delivery_id == 1
    assert created_delivery.order_id == 101
    assert created_delivery.status == DeliveryStatus.PENDING
    assert len(service.deliveries) == 1


def test_create_delivery_raises_error_for_duplicate_id(service, sample_delivery):
    service.create_delivery(sample_delivery)

    with pytest.raises(ValueError, match="already exists"):
        service.create_delivery(sample_delivery)


def test_get_delivery_returns_existing_delivery(service, sample_delivery):
    service.create_delivery(sample_delivery)

    result = service.get_delivery(1)

    assert result is not None
    assert result.delivery_id == 1


def test_get_delivery_returns_none_for_missing_delivery(service):
    result = service.get_delivery(999)

    assert result is None


def test_get_all_deliveries_returns_all_saved_deliveries(service):
    delivery_1 = DeliverySchema(
        delivery_id=1,
        order_id=101,
        status=DeliveryStatus.PENDING,
    )
    delivery_2 = DeliverySchema(
        delivery_id=2,
        order_id=102,
        status=DeliveryStatus.ASSIGNED,
    )

    service.create_delivery(delivery_1)
    service.create_delivery(delivery_2)

    results = service.get_all_deliveries()

    assert len(results) == 2
    assert results[0].delivery_id == 1
    assert results[1].delivery_id == 2


def test_update_delivery_status_updates_status_and_eta(service, sample_delivery):
    service.create_delivery(sample_delivery)

    update_data = DeliveryStatusUpdateSchema(
        status=DeliveryStatus.ON_THE_WAY,
        estimated_arrival="12 minutes",
    )

    updated_delivery = service.update_delivery_status(1, update_data)

    assert updated_delivery is not None
    assert updated_delivery.status == DeliveryStatus.ON_THE_WAY
    assert updated_delivery.estimated_arrival == "12 minutes"


def test_update_delivery_status_returns_none_if_delivery_missing(service):
    update_data = DeliveryStatusUpdateSchema(
        status=DeliveryStatus.DELIVERED,
        estimated_arrival="0 minutes",
    )

    result = service.update_delivery_status(999, update_data)

    assert result is None


def test_assign_driver_sets_driver_info_and_status(service, sample_delivery):
    service.create_delivery(sample_delivery)

    updated_delivery = service.assign_driver(
        delivery_id=1,
        driver_name="Jordan",
        driver_contact="555-6789",
    )

    assert updated_delivery is not None
    assert updated_delivery.driver_name == "Jordan"
    assert updated_delivery.driver_contact == "555-6789"
    assert updated_delivery.status == DeliveryStatus.ASSIGNED


def test_assign_driver_returns_none_for_missing_delivery(service):
    result = service.assign_driver(
        delivery_id=999,
        driver_name="Jordan",
        driver_contact="555-6789",
    )

    assert result is None


def test_delete_delivery_returns_true_when_deleted(service, sample_delivery):
    service.create_delivery(sample_delivery)

    deleted = service.delete_delivery(1)

    assert deleted is True
    assert service.get_delivery(1) is None


def test_delete_delivery_returns_false_when_missing(service):
    deleted = service.delete_delivery(999)

    assert deleted is False