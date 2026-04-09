# backend/routes/admin_router.py

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from backend.repositories.user_repository import UserRepository
from backend.repositories.notifications_repository import NotificationRepository
from backend.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])

user_repo = UserRepository()
notification_repo = NotificationRepository()
admin_service = AdminService(user_repo, notification_repo)


# ── Request bodies ────────────────────────────────────────────────────────────

class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


# ── User endpoints ────────────────────────────────────────────────────────────

@router.get("/users")
def list_users(
    role: Optional[str] = Query(None),
    is_suspended: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("username"),
    sort_order: str = Query("asc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List all users with filtering, sorting, and pagination."""
    return admin_service.get_all_users(
        role=role,
        is_suspended=is_suspended,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )


@router.get("/users/{user_id}")
def get_user(user_id: str):
    """Get a single user by ID."""
    try:
        return admin_service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/users/{user_id}")
def update_user(user_id: str, body: UpdateUserRequest):
    """Update allowed fields on a user."""
    try:
        updates = {k: v for k, v in body.model_dump().items()
                   if v is not None}
        return admin_service.update_user(user_id, updates)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/users/{user_id}/suspend")
def suspend_user(user_id: str):
    """Suspend a user account."""
    try:
        return admin_service.suspend_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/users/{user_id}/unsuspend")
def unsuspend_user(user_id: str):
    """Unsuspend a user account."""
    try:
        return admin_service.unsuspend_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    """Delete a user."""
    try:
        return admin_service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Order endpoints ───────────────────────────────────────────────────────────

@router.get("/orders")
def list_orders(
    status: Optional[str] = Query(None),
    restaurant_id: Optional[int] = Query(None),
    customer_id: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    min_value: Optional[float] = Query(None),
    max_value: Optional[float] = Query(None),
    sort_by: str = Query("order_time"),
    sort_order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List all orders with filtering, sorting, and pagination."""
    return admin_service.get_all_orders(
        status=status,
        restaurant_id=restaurant_id,
        customer_id=customer_id,
        date_from=date_from,
        date_to=date_to,
        min_value=min_value,
        max_value=max_value,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )


# ── Analytics endpoint ────────────────────────────────────────────────────────

@router.get("/analytics")
def get_analytics():
    """Return aggregated metrics for the admin dashboard."""
    return admin_service.get_analytics_summary()