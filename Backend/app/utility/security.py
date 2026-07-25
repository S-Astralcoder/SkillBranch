from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import HTTPException, status
from pwdlib import PasswordHash
import jwt
from app.environment import settings



passwordhash = PasswordHash.recommended()

def get_hashed_password(password : str):
    return passwordhash.hash(password=password)

def verify_password(plain_password : str, hashed_password : str):
    return passwordhash.verify(password=plain_password, hash=hashed_password)

def generate_jwt_token(email : str):
    payload : dict[str, Any] = {"sub" : email}
    if settings.EXPIRATION_MINUTE:
        expiration_date = datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRATION_MINUTE)
        payload.update({"exp" : expiration_date})
    token = jwt.encode(payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def decode_jwt_token(token : str):
    try:
        payload = jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The given token is expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The given token is Invalid")
    if payload:
        return payload
    return False