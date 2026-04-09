# backend/tests/admin/integration_tests/test_admin_routes.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.main import app

client = TestClient(app)

MOCK_USERS = [
    {"id": "1", "username": "alice", "email": "alice@test.com",
     "role": "customer", "is_suspended": False},
    {"id": "2", "username": "bob", "email": "bob@test.com",
     "role": "owner", "is_suspended": False},
]


def test_list_users_returns_200():
    with patch(
        "backend.routes.admin_router.admin_service.get_all_users",
        return_value={
            "users": MOCK_USERS, "total": 2,
            "page": 1, "page_size": 20, "total_pages": 1
        }
    ):
        response = client.get("/admin/users")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2


def test_list_users_with_role_filter():
    with patch(
        "backend.routes.admin_router.admin_service.get_all_users",
        return_value={
            "users": [MOCK_USERS[0]], "total": 1,
            "page": 1, "page_size": 20, "total_pages": 1
        }
    ):
        response = client.get("/admin/users?role=customer")
        assert response.status_code == 200
        assert response.json()["total"] == 1


def test_suspend_user_returns_updated():
    suspended = {**MOCK_USERS[0], "is_suspended": True}
    with patch(
        "backend.routes.admin_router.admin_service.suspend_user",
        return_value=suspended
    ):
        response = client.post("/admin/users/1/suspend")
        assert response.status_code == 200
        assert response.json()["is_suspended"] is True


def test_suspend_admin_returns_400():
    with patch(
        "backend.routes.admin_router.admin_service.suspend_user",
        side_effect=ValueError("Cannot suspend an admin account")
    ):
        response = client.post("/admin/users/3/suspend")
        assert response.status_code == 400


def test_get_analytics_returns_200():
    mock_summary = {
        "total_users": 2, "suspended_users": 0,
        "total_orders": 100, "total_revenue": 5000.00,
        "avg_order_value": 50.00, "total_notifications": 5,
        "top_restaurants": [], "orders_by_month": []
    }
    with patch(
        "backend.routes.admin_router.admin_service.get_analytics_summary",
        return_value=mock_summary
    ):
        response = client.get("/admin/analytics")
        assert response.status_code == 200
        assert response.json()["total_orders"] == 100


def test_list_orders_returns_200():
    with patch(
        "backend.routes.admin_router.admin_service.get_all_orders",
        return_value={
            "orders": [], "total": 0,
            "page": 1, "page_size": 20, "total_pages": 1
        }
    ):
        response = client.get("/admin/orders")
        assert response.status_code == 200


def test_get_user_not_found_returns_404():
    with patch(
        "backend.routes.admin_router.admin_service.get_user_by_id",
        side_effect=ValueError("User 999 not found")
    ):
        response = client.get("/admin/users/999")
        assert response.status_code == 404