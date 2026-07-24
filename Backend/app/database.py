from sqlalchemy import create_engine
from sqlalchemy.orm import Session


# Internal

from models import Base

DATABASE_URL = "sqlite:////C:/Users/blaze/Work Space/Projects/Projects/SkillBranch/Backend/database/skilltree.db"

engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)

def get_database_session():
    with Session(engine) as session, session.begin():
        yield session


