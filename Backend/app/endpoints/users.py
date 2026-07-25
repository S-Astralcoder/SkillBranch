# External
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import re

# Internal
from app.schema import Token, UserRequest
from app.database import get_database_session

from app.models import User
from app.utility.security import generate_jwt_token, get_hashed_password, verify_password
from app.utility.user_utility import does_user_exists, search_user_data


user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post("/login")
async def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db_session : Annotated[Session, Depends(get_database_session)]):
    form_data.username = form_data.username.lower().strip()
    if  not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", form_data.username):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The Username field should contain email address")
    user_data = search_user_data(email=form_data.username, db_session=db_session)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not verify_password(plain_password=form_data.password, hashed_password=user_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    token = generate_jwt_token(email=user_data.email)
    return Token(access_token=token)
    
@user_router.post("/signup")
async def signup(user_data : UserRequest, db_session : Annotated[Session, Depends(get_database_session)]) -> Token:
    user_data.email = user_data.email.lower().strip()

    user = User(username=user_data.username.strip(), email=user_data.email, password=get_hashed_password(user_data.password))
    search_result = does_user_exists(email=user.email, db_session=db_session)
    if search_result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The User Already Exists")
    db_session.add(user)
    token = generate_jwt_token(email=user.email)
    return Token(access_token=token)








