# backend/routes/user_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.repositories.user_repository import UserRepository
from backend.services.feat1.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_service() -> UserService:
    """Create a UserService instance (avoids module-level tight coupling)."""
    return UserService(UserRepository())


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str
    new_password: str


@router.post("/register")
def register_user(request: RegisterRequest):
    try:
        user = get_service().create_user(
            username=request.username,
            email=request.email,
            password=request.password,
        )
        return {
            "message": "user registered successfully",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login_user(request: LoginRequest):
    try:
        user = get_service().authenticate_user(
            username=request.username,
            password=request.password,
        )
        return {
            "message": "login successful",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    try:
        get_service().forgot_password(
            email=request.email,
            new_password=request.new_password,
        )
        return {"message": "password reset successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    