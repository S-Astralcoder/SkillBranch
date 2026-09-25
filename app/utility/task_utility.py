from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Project, Task
from app.utility.check_query import (
    get_project_by_id,
    get_skill_by_id,
    get_task_by_id,
)


def require_project_for_task(
    project_id: UUID,
    skill_id: UUID,
    user_id: UUID,
    db_session: Session,
) -> Project:
    if not get_skill_by_id(
        skill_id=skill_id,
        user_id=user_id,
        db_session=db_session,
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The give skill doesn't exists",
        )

    project = get_project_by_id(
        project_id=project_id,
        skill_id=skill_id,
        user_id=user_id,
        db_session=db_session,
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The give project doesn't exists",
        )
    return project


def require_task_by_id(
    task_id: UUID,
    project_id: UUID,
    skill_id: UUID,
    user_id: UUID,
    db_session: Session,
) -> Task:
    task = get_task_by_id(
        task_id=task_id,
        project_id=project_id,
        skill_id=skill_id,
        user_id=user_id,
        db_session=db_session,
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The given task doesn't exist",
        )
    return task
