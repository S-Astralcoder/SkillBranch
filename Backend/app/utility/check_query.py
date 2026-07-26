from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Project, Skill, Task


def get_skill_by_id(
    skill_id: UUID,
    user_id: UUID,
    db_session: Session,
) -> Skill | None:
    query = select(Skill).where(
        Skill.id == skill_id,
        Skill.user_id == user_id,
    )
    return db_session.scalar(query)


def get_skill_by_name(
    skill_name: str,
    user_id: UUID,
    db_session: Session,
) -> Skill | None:
    query = select(Skill).where(
        Skill.user_id == user_id,
        Skill.skill_name == skill_name,
    )
    return db_session.scalar(query)


def get_project_by_id(
    project_id: UUID,
    skill_id: UUID,
    user_id: UUID,
    db_session: Session,
) -> Project | None:
    query = (
        select(Project)
        .join(Skill, Project.skill_id == Skill.id)
        .where(
            Skill.user_id == user_id,
            Skill.id == skill_id,
            Project.id == project_id,
        )
    )
    return db_session.scalar(query)


def get_project_by_name(
    project_name: str,
    skill_id: UUID,
    user_id: UUID,
    db_session: Session,
) -> Project | None:
    query = (
        select(Project)
        .join(Skill, Project.skill_id == Skill.id)
        .where(
            Skill.user_id == user_id,
            Skill.id == skill_id,
            Project.project_name == project_name,
        )
    )
    return db_session.scalar(query)


def get_task_by_id(
    task_id: UUID,
    project_id: UUID,
    skill_id: UUID,
    user_id: UUID,
    db_session: Session,
) -> Task | None:
    query = (
        select(Task)
        .join(Project, Project.id == Task.project_id)
        .join(Skill, Skill.id == Project.skill_id)
        .where(
            Skill.user_id == user_id,
            Task.id == task_id,
            Project.id == project_id,
            Skill.id == skill_id,
        )
    )
    return db_session.scalar(query)


def get_task_by_name(
    task_name: str,
    project_id: UUID,
    skill_id: UUID,
    user_id: UUID,
    db_session: Session,
) -> Task | None:
    query = (
        select(Task)
        .join(Project, Project.id == Task.project_id)
        .join(Skill, Skill.id == Project.skill_id)
        .where(
            Skill.user_id == user_id,
            Task.task_name == task_name,
            Project.id == project_id,
            Skill.id == skill_id,
        )
    )
    return db_session.scalar(query)


def get_tasks_by_project(
    project_id: UUID,
    skill_id: UUID,
    user_id: UUID,
    db_session: Session,
    offset: int,
    limit: int | None,
) -> list[Task]:
    query = (
        (
            select(Task)
            .join(Project, Project.id == Task.project_id)
            .join(Skill, Skill.id == Project.skill_id)
            .where(
                Skill.user_id == user_id,
                Project.id == project_id,
                Skill.id == skill_id,
            )
        )
        .offset(offset=offset)
        .limit(limit=limit)
    )
    return list(db_session.scalars(query).all())


def get_tasks_ordered_by_deadline(
    user_id: UUID,
    db_session: Session,
) -> list[Task]:
    query = (
        select(Task)
        .join(Project, Project.id == Task.project_id)
        .join(Skill, Skill.id == Project.skill_id)
        .where(Skill.user_id == user_id, Task.completed == False)  # noqa
        .order_by(Task.deadline.asc())
    )
    return list(db_session.scalars(query).all())
