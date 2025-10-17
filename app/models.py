"""
module: models.py
purpose: pydantic validation schemas
"""

from pydantic import BaseModel, field_validator, EmailStr, SecretStr, model_validator
from typing import Optional
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

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

    @model_validator(mode="after")
    def validate_fields(self):
        if self.username is None and self.email is None:
            raise ValueError("at least one field should be passed")
        return self
