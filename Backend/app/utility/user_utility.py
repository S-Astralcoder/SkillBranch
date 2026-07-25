# External
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

# Internal
from app.database import get_database_session
from app.models import User
from app.utility.security import decode_jwt_token

authorization = OAuth2PasswordBearer(tokenUrl="/user/login")



def search_user_data(email : str, db_session : Session) -> User:
    user_data = db_session.scalar((select(User).where(User.email == email)))
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Doesn't Exists")
    return user_data

def does_user_exists(email : str, db_session : Session) -> bool:
    user_data = db_session.scalar((select(User).where(User.email == email)))
    if user_data:
        return True
    return False 


def get_current_active_user(token : Annotated[str, Depends(authorization)], db_session : Annotated[Session, Depends(get_database_session)]):
    jwt_decoded_data = decode_jwt_token(token=token)
    if not jwt_decoded_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT Token")
    email = jwt_decoded_data.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This jwt token doesn't contain email")
    user = search_user_data(email=email, db_session=db_session)
    return user
    
    

    