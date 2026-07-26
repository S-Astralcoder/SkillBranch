from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session


# Internal

from app.environment import settings
from app.models import Base

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


Base.metadata.create_all(engine)


def get_database_session():
    with Session(engine) as session:
        yield session
        session.commit()
