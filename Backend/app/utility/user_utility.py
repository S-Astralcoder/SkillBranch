from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_database_session
from app.models import User
from app.utility.security import decode_jwt_token

authorization = OAuth2PasswordBearer(tokenUrl="/user/login")


def normalize_email(email: str) -> str:
    return email.lower().strip()


def get_user_by_email(email: str, db_session: Session) -> User | None:
    return db_session.scalar(select(User).where(User.email == email))


def require_user_by_email(email: str, db_session: Session) -> User:
    user = get_user_by_email(email=email, db_session=db_session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Doesn't Exists",
        )
    return user


def user_exists(email: str, db_session: Session) -> bool:
    return get_user_by_email(email=email, db_session=db_session) is not None


def get_current_active_user(
    token: Annotated[str, Depends(authorization)],
    db_session: Annotated[Session, Depends(get_database_session)],
) -> User:
    jwt_decoded_data = decode_jwt_token(token=token)
    if not jwt_decoded_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT Token",
        )
    email = jwt_decoded_data.get("sub")  # pyright: ignore
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This jwt token doesn't contain email",
        )
    return require_user_by_email(email=email, db_session=db_session)  # pyright: ignore
