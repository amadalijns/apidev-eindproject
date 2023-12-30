import crud
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key
SECRET_KEY = "e2fafc62dfd637c751a3d9ea2ef2b0e9e525ae58e8c2a4804fff20464daf1bd6"

# Gebruikte algorithme
ALGORITHM = "HS256"

# Tijdslimiet voor de access token
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


# Functie om het wachtwoord te hashen
def get_password_hash(password):
    return pwd_context.hash(password)


# Functie om het wachtwoord te controleren
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Functie om een user te authenticeren
def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Functie om een access token te maken
def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
