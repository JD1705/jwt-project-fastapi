from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.security import verify_token
from app.database import get_collection
from bson import ObjectId

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    try:
        token = credentials.credentials
        payload = verify_token(token)

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Token: it does not have user_id"
                    )
        
        collection = get_collection("users")
        user = collection.find_one({"_id":ObjectId(user_id)})
        if not user:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User Not Found"
                    )

        return user

    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User could not be authenticated"
                )
