from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_database_session
from app.models import Project, Skill, Task, User
from app.schema import CreateTask, TaskRequest, TasksRequest, ToggleTaskRequest, UpdateTask
from app.utility.check_query import get_project_by_id, get_skill_by_id, get_task_by_id, get_task_by_name
from app.utility.user_utility import get_current_active_user


task_router = APIRouter(prefix="/task", tags=["Task"])


@task_router.post("/tasks")
async def get_all_tasks(payload : TasksRequest, user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session, Depends(get_database_session)]):
    if not get_skill_by_id(skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give skill doesn't exists")
    if not  get_project_by_id(project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give project doesn't exists")
    query = select(Task).join(Project, Project.id == Task.project_id).join(Skill, Skill.id == Project.skill_id).where(Skill.user_id == user.id, Project.id == payload.project_id, Skill.id == payload.skill_id)
    return db_session.scalars(query).all()

@task_router.post("/task")
async def get_task(payload : TaskRequest, user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session, Depends(get_database_session)]):
    if not get_skill_by_id(skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give skill doesn't exists")
    project = get_project_by_id(project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give project doesn't exists")
    task = get_task_by_id(task_id=payload.task_id, project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given task doesn't exist")
    return task

@task_router.post("/create_task")
async def create_task(payload : CreateTask, user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session, Depends(get_database_session)]):
    if not get_skill_by_id(skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give skill doesn't exists")
    project = get_project_by_id(project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give project doesn't exists")
    if get_task_by_name(task_name=payload.task_name, project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The given task already exists")
    
    task = Task(task_name=payload.task_name, description=payload.description, deadline=payload.deadline, project_id=project.id)
    db_session.add(task)
    db_session.flush()
    return task


@task_router.put("/update_task")
async def update_task(payload : UpdateTask, user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session, Depends(get_database_session)]):
    if not get_skill_by_id(skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give skill doesn't exists")
    if not get_project_by_id(project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give project doesn't exists")
    task_with_name = get_task_by_name(task_name=payload.task_name, project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session)
    if task_with_name and task_with_name.id != payload.task_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The given task already exists")
    task = get_task_by_id(task_id=payload.task_id, project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given task doesn't exist")
    task.task_name = payload.task_name
    task.description = payload.description
    task.deadline = payload.deadline
    return task

@task_router.delete("/delete_task")
async def delete_task(payload : TaskRequest, user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session, Depends(get_database_session)]):
    if not get_skill_by_id(skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give skill doesn't exists")
    project = get_project_by_id(project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give project doesn't exists")
    task = get_task_by_id(task_id=payload.task_id, project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given task doesn't exist")
    project.tasks.remove(task)
    return task

@task_router.patch("/toggle_task")
async def toggle_task(payload : ToggleTaskRequest, user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session, Depends(get_database_session)]):
    if not get_skill_by_id(skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give skill doesn't exists")
    if not get_project_by_id(project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The give project doesn't exists")
    task = get_task_by_id(task_id=payload.task_id, project_id=payload.project_id, skill_id=payload.skill_id, user_id=user.id, db_session=db_session)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given task doesn't exist")
    task.completed = payload.toggle
    return task

@task_router.post("/near_deadline_tasks")
async def get_near_deadline_tasks(user : Annotated[User, Depends(get_current_active_user)], db_session : Annotated[Session, Depends(get_database_session)]):
    query = select(Task).join(Project, Project.id == Task.project_id).join(Skill, Skill.id == Project.skill_id).where(Skill.user_id == user.id).order_by(Task.deadline.desc())
    return db_session.scalars(query).all()

