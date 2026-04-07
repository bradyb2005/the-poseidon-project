from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.repositories.notifications_repository import NotificationRepository
from backend.services.notifications_services import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])

notification_repo = NotificationRepository()
notification_service = NotificationService(notification_repo)


class NotificationPreferenceRequest(BaseModel):
    user_id: str
    notification_type: str
    enabled: bool


class OrderStatusNotificationRequest(BaseModel):
    user_id: str
    order_id: str
    status: str


class PaymentStatusNotificationRequest(BaseModel):
    user_id: str
    order_id: str
    success: bool


class NewOrderNotificationRequest(BaseModel):
    owner_id: str
    order_id: str


class FlaggedReviewNotificationRequest(BaseModel):
    admin_id: str
    review_id: str


class NewReviewNotificationRequest(BaseModel):
    owner_id: str
    review_id: str


@router.get("/{user_id}")
def get_notifications(user_id: str):
    return {
        "notifications": notification_service.get_notifications_for_user(user_id)
    }


@router.put("/preferences")
def set_notification_preference(request: NotificationPreferenceRequest):
    try:
        result = notification_service.set_notification_enabled(
            user_id=request.user_id,
            notification_type=request.notification_type,
            enabled=request.enabled,
        )
        return {
            "message": "notification preference updated",
            "preference": result,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/trigger/order-status")
def trigger_order_status_notification(request: OrderStatusNotificationRequest):
    notification = notification_service.notify_order_status_change(
        user_id=request.user_id,
        order_id=request.order_id,
        status=request.status,
    )

    if notification is None:
        return {"message": "order status notifications are disabled for this user"}

    return {
        "message": "order status notification created",
        "notification": notification,
    }


@router.post("/trigger/payment-status")
def trigger_payment_status_notification(request: PaymentStatusNotificationRequest):
    notification = notification_service.notify_payment_status(
        user_id=request.user_id,
        order_id=request.order_id,
        success=request.success,
    )

    if notification is None:
        return {"message": "payment status notifications are disabled for this user"}

    return {
        "message": "payment status notification created",
        "notification": notification,
    }


@router.post("/trigger/new-order")
def trigger_new_order_notification(request: NewOrderNotificationRequest):
    notification = notification_service.notify_restaurant_new_order(
        owner_id=request.owner_id,
        order_id=request.order_id,
    )

    if notification is None:
        return {"message": "new order notifications are disabled for this user"}

    return {
        "message": "new order notification created",
        "notification": notification,
    }


@router.post("/trigger/flagged-review")
def trigger_flagged_review_notification(request: FlaggedReviewNotificationRequest):
    notification = notification_service.notify_admin_flagged_review(
        admin_id=request.admin_id,
        review_id=request.review_id,
    )

    if notification is None:
        return {"message": "flagged review notifications are disabled for this user"}

    return {
        "message": "flagged review notification created",
        "notification": notification,
    }


@router.post("/trigger/new-review")
def trigger_new_review_notification(request: NewReviewNotificationRequest):
    notification = notification_service.notify_restaurant_new_review(
        owner_id=request.owner_id,
        review_id=request.review_id,
    )

    if notification is None:
        return {"message": "new review notifications are disabled for this user"}

    return {
        "message": "new review notification created",
        "notification": notification,
    }