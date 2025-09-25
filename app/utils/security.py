import bcrypt

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
