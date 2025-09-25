import bcrypt

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    bytes_password = password.encode()

    hashed_password = bcrypt.hashpw(bytes_password, salt)
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pass
