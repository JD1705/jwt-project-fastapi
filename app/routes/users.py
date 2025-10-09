from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user
from app.models import UserResponse

router = APIRouter(prefix="/users")

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: dict = Depends(get_current_user)) -> UserResponse:
    response = UserResponse(
            id=str(current_user["_id"]),
            email=current_user["email"],
            username=current_user["username"],
            created_at=current_user["created_at"]
            )

    return response
