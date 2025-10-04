import jwt
import bcrypt
from datetime import timedelta, timezone, datetime
import os
from dotenv import load_dotenv

load_dotenv()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    bytes_password = password.encode()

    hashed_password = bcrypt.hashpw(bytes_password, salt)

    hashed_password_str = hashed_password.decode()
    return hashed_password_str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password_bytes = plain_password.encode()
    hashed_password_bytes = hashed_password.encode()

    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

# JWT utility functions

def create_access_token(data: dict, expire_delta: None|timedelta = None) -> str:
    to_encode = data.copy()

    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_TIME", 30))
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    to_encode.update({"exp":expire})
    
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("SECRET_KEY is not configured in the environment variables")

    algorithm = os.getenv("ALGORITHM")

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm)

    return encoded_jwt
