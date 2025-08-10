from passlib.context import CryptContext
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import hashlib

# Use a strong random secret key for production!
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

# Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = hashlib

def hash_password(password: str) -> str:
    
    return pwd_context.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_token(data: dict, expires_minutes: int = 300) -> str:
    """
    Create a JWT token with given payload and expiry.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
