import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_database_session
from app.models import Task, User
from app.schema import (
    CreateTask,
    TaskRequest,
    ToggleTaskRequest,
    UpdateTask,
)
from app.utility.check_query import (
    get_task_by_name,
    get_tasks_by_project,
    get_tasks_ordered_by_deadline,
)
from app.utility.task_utility import require_project_for_task, require_task_by_id
from app.utility.user_utility import get_current_active_user

task_router = APIRouter(prefix="/task", tags=["Task"])


@task_router.get("/tasks/{skill_id}/{project_id}")
async def get_all_tasks(
    skill_id: uuid.UUID,
    project_id: uuid.UUID,
    user: Annotated[User, Depends(get_current_active_user)],
    db_session: Annotated[Session, Depends(get_database_session)],
    offset: int = 0,
    limit: int | None = None,
):
    require_project_for_task(
        project_id=project_id,
        skill_id=skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    return get_tasks_by_project(
        project_id=project_id,
        skill_id=skill_id,
        user_id=user.id,
        db_session=db_session,
        offset=offset,
        limit=limit,
    )


@task_router.get("/task/{skill_id}/{project_id}/{task_id}")
async def get_task(
    skill_id: uuid.UUID,
    project_id: uuid.UUID,
    task_id: uuid.UUID,
    user: Annotated[User, Depends(get_current_active_user)],
    db_session: Annotated[Session, Depends(get_database_session)],
):
    require_project_for_task(
        project_id=project_id,
        skill_id=skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    return require_task_by_id(
        task_id=task_id,
        project_id=project_id,
        skill_id=skill_id,
        user_id=user.id,
        db_session=db_session,
    )


@task_router.post("/create_task")
async def create_task(
    payload: CreateTask,
    user: Annotated[User, Depends(get_current_active_user)],
    db_session: Annotated[Session, Depends(get_database_session)],
):
    project = require_project_for_task(
        project_id=payload.project_id,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    if get_task_by_name(
        task_name=payload.task_name,
        project_id=payload.project_id,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    ):
        raise HTTPException(
            status_code=status.HTTP_306_RESERVED,
            detail="The given task already exists",
        )

    task = Task(
        task_name=payload.task_name,
        description=payload.description,
        deadline=payload.deadline,
        project_id=project.id,
    )
    db_session.add(task)
    db_session.flush()
    return task


@task_router.put("/update_task")
async def update_task(
    payload: UpdateTask,
    user: Annotated[User, Depends(get_current_active_user)],
    db_session: Annotated[Session, Depends(get_database_session)],
):
    require_project_for_task(
        project_id=payload.project_id,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    task_with_name = get_task_by_name(
        task_name=payload.task_name,
        project_id=payload.project_id,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    if task_with_name and task_with_name.id != payload.task_id:
        raise HTTPException(
            status_code=status.HTTP_306_RESERVED,
            detail="The given task already exists",
        )

    task = require_task_by_id(
        task_id=payload.task_id,
        project_id=payload.project_id,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    task.task_name = payload.task_name
    task.description = payload.description
    task.deadline = payload.deadline
    return task


@task_router.delete("/delete_task")
async def delete_task(
    payload: TaskRequest,
    user: Annotated[User, Depends(get_current_active_user)],
    db_session: Annotated[Session, Depends(get_database_session)],
):
    project = require_project_for_task(
        project_id=payload.project_id,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    task = require_task_by_id(
        task_id=payload.task_id,
        project_id=payload.project_id,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    project.tasks.remove(task)
    return task


@task_router.patch("/toggle_task")
async def toggle_task(
    payload: ToggleTaskRequest,
    user: Annotated[User, Depends(get_current_active_user)],
    db_session: Annotated[Session, Depends(get_database_session)],
):
    require_project_for_task(
        project_id=payload.project_id,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    task = require_task_by_id(
        task_id=payload.task_id,
        project_id=payload.project_id,
        skill_id=payload.skill_id,
        user_id=user.id,
        db_session=db_session,
    )
    task.completed = payload.toggle
    return task


@task_router.get("/near_deadline_tasks")
async def get_near_deadline_tasks(
    user: Annotated[User, Depends(get_current_active_user)],
    db_session: Annotated[Session, Depends(get_database_session)],
):
    return get_tasks_ordered_by_deadline(
        user_id=user.id,
        db_session=db_session,
    )
