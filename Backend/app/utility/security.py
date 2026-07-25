from datetime import datetime, timedelta
from pwdlib import PasswordHash
import jwt
from app.environment import settings



passwordhash = PasswordHash.recommended()

def get_hashed_password(password : str):
    return passwordhash.hash(password=password)

def verify_password(plain_password : str, hashed_password : str):
    return passwordhash.verify(password=plain_password, hash=hashed_password)

def generate_jwt_token(email : str):
    payload = {"sub" : email}
    if settings.EXPIRATION_MINUTE:
        payload.update({"exp" : f"{datetime.now() + timedelta(minutes=settings.EXPIRATION_MINUTE)}"})
    token = jwt.encode(payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def decode_jwt_token_to_email(token : str):
    payload = jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM)
    if payload:
        return payload.get("sub")
    return False