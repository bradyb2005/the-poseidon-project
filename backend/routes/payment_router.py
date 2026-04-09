# backend/routes/payment_router.py
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status, Body

from backend.schemas.payment_schema import (
    CostBreakdown,
    PaymentSchema,
)
from backend.services.payment_service import PaymentService

service = PaymentService()

router = APIRouter(prefix="/payments", tags=["payments"])


# --- Feature 6: Cost Calculation Methods ---

@router.post("/subtotal", response_model=Dict[str, float], status_code=status.HTTP_200_OK)
def post_calculate_subtotal(order: Any = Body(...)):
    """
    POST: Calculate subtotal from an order
    """
    try:
        subtotal = service.calculate_subtotal(order)
        return {"subtotal": subtotal}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/fees-taxes", response_model=Dict[str, float], status_code=status.HTTP_200_OK)
def post_calculate_fees_and_taxes(subtotal: float = Body(...)):
    """
    POST: Calculate delivery fee, service fee, and tax from subtotal
    """
    try:
        return service.calculate_fees_and_taxes(subtotal)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/total", response_model=CostBreakdown, status_code=status.HTTP_200_OK)
def post_calculate_total(subtotal: float = Body(...)):
    """
    POST: Calculate full cost breakdown from subtotal
    """
    try:
        return service.calculate_total(subtotal)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# --- Feature 7: Payment Processing Methods ---

@router.post("/info", response_model=Dict, status_code=status.HTTP_200_OK)
def post_retrieve_payment_info(payload: PaymentSchema):
    """
    POST: Retrieve payment information from payment schema
    """
    try:
        return service.retrieve_payment_info(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/process", response_model=PaymentSchema, status_code=status.HTTP_200_OK)
def post_process_payment(payload: PaymentSchema):
    """
    POST: Process payment through payment service
    """
    try:
        return service.process_payment(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/fulfillment", response_model=Dict, status_code=status.HTTP_200_OK)
def post_create_fulfillment_request(payload: PaymentSchema):
    """
    POST: Create fulfillment request for accepted payment
    """
    try:
        return service.create_fulfillment_request(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )