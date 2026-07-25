
import uuid
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.models import Project, Skill


def check_if_skill_name_exists(skill_name : str, user_id : uuid.UUID ,db_session : Session):
    result = db_session.scalar(select(Skill).where(Skill.user_id == user_id, Skill.skill_name == skill_name))
    if result:
        return result.id
    return False

def check_if_project_name_already_exists(project_name : str ,skill_id : uuid.UUID, user_id : uuid.UUID , db_session : Session):
    query = select(Project).join(Skill, Project.skill_id == Skill.id).where(Skill.user_id == user_id, Skill.id == skill_id, Project.project_name == project_name)
    project = db_session.scalar(query)
    if project:
        return project.id
    return False

def check_if_skill_exists( skill_id : uuid.UUID, user_id : uuid.UUID , db_session : Session):
    query = select(Skill).options(joinedload(Skill.projects)).where(Skill.id == skill_id, Skill.user_id == user_id)
    skill = db_session.scalar(query)
    if skill:
        return skill
    return False