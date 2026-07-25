from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_database_session
from app.models import Skill, User
from app.utility.user_utility import get_current_active_user



skill_router = APIRouter(prefix="/skill", tags=["Skill"])


@skill_router.get("/skills")
async def get_all_skills(user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)], offset : int = 0 , limit : int | None = None):
    get_skills_query = select(Skill).where(Skill.user_id == user.id).offset(offset=offset).limit(limit=limit)
    skills_data = db_session.execute(get_skills_query).all()
    return skills_data

@skill_router.get(f"skill/{id}")
async def get_skill():
    pass

async def create_skill():
    pass

async def update_skill():
    pass
