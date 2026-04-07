from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routes.delivery_router import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_create_delivery_route():
    response = client.post(
        "/deliveries/",
        json={
            "delivery_id": 1,
            "order_id": 101,
            "status": "pending",
            "estimated_arrival": "30 minutes",
            "driver_name": None,
            "driver_contact": None,
        },
    )

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["delivery_id"] == 1
    assert response_data["order_id"] == 101
    assert response_data["status"] == "pending"


def test_create_delivery_route_rejects_duplicate_id():
    client.post(
        "/deliveries/",
        json={
            "delivery_id": 2,
            "order_id": 102,
            "status": "pending",
        },
    )

    response = client.post(
        "/deliveries/",
        json={
            "delivery_id": 2,
            "order_id": 103,
            "status": "assigned",
        },
    )

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_all_deliveries_route():
    client.post(
        "/deliveries/",
        json={
            "delivery_id": 3,
            "order_id": 103,
            "status": "pending",
        },
    )
    client.post(
        "/deliveries/",
        json={
            "delivery_id": 4,
            "order_id": 104,
            "status": "assigned",
        },
    )

    response = client.get("/deliveries/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2


def test_get_delivery_route():
    client.post(
        "/deliveries/",
        json={
            "delivery_id": 5,
            "order_id": 105,
            "status": "assigned",
        },
    )

    response = client.get("/deliveries/5")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["delivery_id"] == 5
    assert response_data["order_id"] == 105
    assert response_data["status"] == "assigned"


def test_get_delivery_route_returns_404_for_missing_delivery():
    response = client.get("/deliveries/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Delivery not found."


def test_update_delivery_status_route():
    client.post(
        "/deliveries/",
        json={
            "delivery_id": 6,
            "order_id": 106,
            "status": "pending",
        },
    )

    response = client.put(
        "/deliveries/6/status",
        json={
            "status": "on_the_way",
            "estimated_arrival": "8 minutes",
        },
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "on_the_way"
    assert response_data["estimated_arrival"] == "8 minutes"


def test_update_delivery_status_route_returns_404_for_missing_delivery():
    response = client.put(
        "/deliveries/999/status",
        json={
            "status": "delivered",
            "estimated_arrival": "0 minutes",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Delivery not found."