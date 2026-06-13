
import bcrypt
from fastapi import Header
from jose import jwt , JWTError
from datetime import datetime , timedelta , timezone

SECRET_KEY = "mybookreadingtracker@2026#secure"
ALGORITHM = "HS256"

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None