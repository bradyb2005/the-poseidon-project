from __future__ import annotations

from enum import Enum
from typing import Optional

from backend.models.user.user_model import User


class ReviewModerationAction(str, Enum):
    DELETE = "delete"
    RECOVER = "recover"
    FLAG = "flag"
    UNFLAG = "unflag"


class Admin(User):
    """
    Admin model should be small: only admin-specific actions.

    Anything involving orders/menus/restaurants/search/pagination should live
    in the relevant model/service layer (SRP).
    """

    def modify_credentials(
        self,
        user: User,
        new_username: Optional[str] = None,
        new_password: Optional[str] = None,
    ) -> None:
        # Username uniqueness should be enforced by a service/repository,
        # not the Admin model (Admin has no DB context).
        if new_username is not None:
            if not isinstance(new_username, str) or not new_username.strip():
                raise ValueError("username must be a non-empty string")
            user.username = new_username.strip()

        if new_password is not None:
            user.password_hash = User.hash_password(new_password)

    def moderate_review(self, review: "Review", action: ReviewModerationAction) -> None:
        """
        Admin requests a moderation action; the Review model should apply state changes.
        We'll call a method if it exists; otherwise set fields as a fallback.
        """
        if hasattr(review, "apply_moderation"):
            review.apply_moderation(action.value)
        else:
            # fallback (kept minimal)
            setattr(review, "moderation_action", action.value)