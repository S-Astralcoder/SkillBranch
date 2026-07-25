# External
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

# Internal
from app.models import User




def search_user_data(email : str, db_session : Session) -> User | None:
    user_data = db_session.execute((select(User).where(User.email == email))).fetchone()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Doesn't Exists")
    return user_data[0]
