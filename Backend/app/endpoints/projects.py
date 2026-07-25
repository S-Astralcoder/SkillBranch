import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_database_session
from app.models import Project, Skill, User
from app.schema import CreateProject, ProjectRequest, ProjectUpdate
from app.utility.check_query import (
    get_project_by_id,
    get_project_by_name,
    get_skill_by_id,
)
from app.utility.user_utility import get_current_active_user

project_router = APIRouter(prefix="/project", tags=["Project"])

@project_router.get("/projects/{skill_id}")
async def get_all_projects(skill_id : uuid.UUID ,user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)], offset : int = 0 , limit : int | None = None):
    if not get_skill_by_id(skill_id=skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given Skill doesn't exist")

    query = select(Project).join(Skill, Project.skill_id == Skill.id).where(Skill.user_id == user.id, Skill.id == skill_id).offset(offset=offset).limit(limit=limit)
    projects = db_session.scalars(query).all()
    return projects

@project_router.get("/project/{skill_id}/{project_id}")
async def get_project(skill_id : uuid.UUID, project_id : uuid.UUID ,user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)]):
    if not get_skill_by_id(skill_id=skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given Skill doesn't exist")

    project = get_project_by_id(
        project_id=project_id,
        skill_id=skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given project doesn't exists")
    return project

@project_router.post("/create_project")
async def create_project( payload : CreateProject ,user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)]):
    skill = get_skill_by_id(skill_id=payload.skill_id, user_id=user.id, db_session=db_session)
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given Skill doesn't exist")
    if get_project_by_name(
        project_name=payload.project_name,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The given project name already exists")
    project = Project(project_name=payload.project_name, description=payload.description, skill_id=skill.id)
    db_session.add(project)
    db_session.flush()
    return project

@project_router.put("/update_project")
async def update_project(payload : ProjectUpdate ,user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)]):
    if not get_skill_by_id(skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given Skill doesn't exist")

    project = get_project_by_id(
        project_id=payload.project_id,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project Does not exists")

    project_with_name = get_project_by_name(
        project_name=payload.project_name,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    if project_with_name and project_with_name.id != project.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The given project name already exists")
    
    project.project_name = payload.project_name
    project.description = payload.description

    db_session.flush()
    return project

@project_router.delete("/delete_project")
async def delete_project(payload : ProjectRequest ,user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session ,Depends(get_database_session)]):
    if not get_skill_by_id(skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given Skill doesn't exist")

    project = get_project_by_id(project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session)

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given project doesn't exists")
    
    skill = get_skill_by_id(skill_id=payload.skill_id, user_id=user.id, db_session=db_session)
    if not skill:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="I don't even know how this was triggered")
    print(skill)
    print(project)
    
    skill.projects.remove(project)
    return project
