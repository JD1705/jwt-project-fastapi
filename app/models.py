from pydantic import BaseModel, field_validator, EmailStr, SecretStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr

    @field_validator("confirm_password")
    def validate_passwords(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("Passwords dont match")
        return v

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    created_at: datetime

class UserDB(BaseModel):
    _id: str
    username: str
    email: EmailStr
    hashed_password: str
    created_at: datetime
    role: str = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr
