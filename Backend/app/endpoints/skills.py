from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_database_session
from app.models import Skill, User
from app.schema import SkillCreateRequest
from app.utility.check_query import check_if_skill_name_exists
from app.utility.user_utility import get_current_active_user



skill_router = APIRouter(prefix="/skill", tags=["Skill"])


@skill_router.get("/skills")
async def get_all_skills(user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)], offset : int = 0 , limit : int | None = None):
    get_skills_query = select(Skill).where(Skill.user_id == user.id).offset(offset=offset).limit(limit=limit)
    skills_data = db_session.scalars(get_skills_query).all()
    return skills_data

@skill_router.get(f"/{id}")
async def get_skill(id : uuid.UUID, user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)]):
    get_skills_query = select(Skill).where(Skill.user_id == user.id, Skill.id == id)
    skills_data = db_session.scalar(get_skills_query)
    return skills_data

@skill_router.post("/create_skill")
async def create_skill(skill_data : SkillCreateRequest, user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)]):
    if check_if_skill_name_exists(skill_name=skill_data.name, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_306_RESERVED, detail="The Skill name already exists")
    skill = Skill(skill_name=skill_data.name, description=skill_data.description, user_id=user.id)
    db_session.add(skill)
    db_session.flush()
    return skill

@skill_router.put(f"/update_skill/{id}")
async def update_skill(id : uuid.UUID, skill_data : SkillCreateRequest, user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)]):
    skill = db_session.scalar(select(Skill).where(Skill.id == id, Skill.user_id == user.id))
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    result = check_if_skill_name_exists(skill_name=skill_data.name, user_id=user.id, db_session=db_session)
    if result and result != skill.id:
        raise HTTPException(status_code=status.HTTP_306_RESERVED, detail="The Skill name already exists")
    skill.skill_name = skill_data.name
    skill.description = skill_data.description
    db_session.flush()
    return skill

@skill_router.put(f"/delete_skill/{id}")
async def delete_skill(id : uuid.UUID, user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)]):
    user_profile = db_session.scalar(select(User).options(joinedload(User.skills)).where(User.id == user.id))
    if user_profile is None:
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail="I don't know how this would happen")
    skill = db_session.scalar(select(Skill).where(Skill.user_id == user.id, Skill.id == id))
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request skill doesn't exists")
    user_profile.skills.remove(skill)
    return skill



