
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Skill


def check_if_skill_name_exists(skill_name : str, user_id : uuid.UUID ,db_session : Session):
    result = db_session.scalar(select(Skill).where(Skill.user_id == user_id, Skill.skill_name == skill_name))
    if result:
        return result.id
    return False