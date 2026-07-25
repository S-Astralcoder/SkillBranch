from sqlalchemy import create_engine
from sqlalchemy.orm import Session


# Internal

from app.environment import settings
from app.models import Base

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)

def get_database_session():
    with Session(engine) as session:
        yield session
        session.commit()


