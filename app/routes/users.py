from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.dependencies import get_current_user
from app.models import UserResponse, UserUpdate
from app.database import get_collection

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

@router.put("/me", response_model=UserResponse)
def update_my_profile(update_data: UserUpdate, current_user: dict = Depends(get_current_user)) -> UserResponse:
    collection = get_collection("users")
    if update_data.username and update_data.email is None:
        collection.update_one({"_id":current_user["_id"]}, {"$set":{"username":update_data.username}})
        
        updated_user = collection.find_one({"_id":current_user["_id"]})
        return UserResponse(
                id=str(updated_user["_id"]),    # type: ignore
                username=updated_user["username"],    # type: ignore
                email=updated_user["email"],    # type: ignore
                created_at=updated_user["created_at"]    # type: ignore
                )

    elif update_data.email and update_data.username is None:
        normalized_email = update_data.email.lower().strip()
        
        user_exists = collection.find_one({"email":normalized_email})
        if not user_exists:
            collection.update_one({"_id":current_user["_id"]}, {"$set":{"email":normalized_email}})
            
            updated_user = collection.find_one({"_id":current_user["_id"]})
            return UserResponse(
                    id=str(updated_user["_id"]),    # type: ignore
                    username=updated_user["username"],     # type: ignore
                    email=updated_user["email"],    # type: ignore
                    created_at=updated_user["created_at"]    # type: ignore
                    )
        else:
            raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Incorrect Credentials"
                    )

    else:
        normalized_email = update_data.email.lower().strip()    # type: ignore

        user_exists = collection.find_one({"email":normalized_email})
        if not user_exists:
            update_dict = {"username":update_data.username, "email":normalized_email}
            collection.update_one({"_id":current_user["_id"]}, {"$set":update_dict})
            
            updated_user = collection.find_one({"_id":current_user["_id"]})
            return UserResponse(
                    id=str(updated_user["_id"]),    # type: ignore
                    username=updated_user["username"],    # type: ignore
                    email=updated_user["email"],    # type: ignore
                    created_at=updated_user["created_at"]    # type: ignore
                    )

        else:
            raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Incorrect Credentials"
                    )
