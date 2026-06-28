from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.dependencies.auth_guard import require_admin_user
from app.models.user_model import User


router = APIRouter(
    prefix="/admin/users",
    tags=["Admin Users"],
    dependencies=[Depends(require_admin_user)],
)


@router.get("", status_code=status.HTTP_200_OK)
def get_admin_users(
    session: Session = Depends(get_session),
):
    users = session.exec(select(User)).all()

    return {
        "message": "Users retrieved successfully",
        "data": [
            {
                "user_id": user.user_id,
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "role": getattr(user, "role", "Customer"),
                "is_active": user.is_active,
                "created_at": user.created_at,
            }
            for user in users
        ],
    }
