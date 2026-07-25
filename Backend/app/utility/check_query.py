
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Project, Skill


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
