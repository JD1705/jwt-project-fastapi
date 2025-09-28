from fastapi import APIRouter, HTTPException, status
from app.models import UserCreate, UserDB, UserResponse
from app.database import get_collection
from app.utils.security import hash_password
from datetime import datetime, timezone
from bson import ObjectId

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate):
    collection = get_collection("users")
    normalized_email = user_data.email.lower().strip()

    existing_user = collection.find_one({"email":normalized_email})
    if existing_user:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exist"
                )
    else:
        hashed_password = hash_password(user_data.password.get_secret_value())
        unique_id = ObjectId()

        new_user = UserDB(
                _id=str(unique_id),
                email=normalized_email,
                username=user_data.username,
                hashed_password=hashed_password,
                created_at=datetime.now(timezone.utc)
                )
 
        collection.insert_one(new_user.model_dump())

        return UserResponse(
                id=str(unique_id),
                username=user_data.username,
                email=user_data.email,
                created_at=datetime.now(timezone.utc)
                )
