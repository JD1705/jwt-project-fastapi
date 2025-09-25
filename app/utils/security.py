import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    bytes_password = password.encode()

    hashed_password = bcrypt.hashpw(bytes_password, salt)

    hashed_password_str = hashed_password.decode()
    return hashed_password_str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pass
