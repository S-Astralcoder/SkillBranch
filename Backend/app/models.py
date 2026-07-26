from __future__ import annotations

import datetime
from uuid import UUID, uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    def __repr__(self):
        cols = ", ".join(
            f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith("_")
        )
        return f"<{self.__class__.__name__}({cols})>"


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
    )

    skills: Mapped[list[Skill]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )


class Skill(Base):
    __tablename__ = "skill"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    skill_name: Mapped[str] = mapped_column(String(400), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    user: Mapped[User] = relationship(back_populates="skills")

    projects: Mapped[list[Project]] = relationship(
        back_populates="skill", cascade="all, delete-orphan", passive_deletes=True
    )

    __table_args__ = (UniqueConstraint("user_id", "skill_name"),)


class Project(Base):
    __tablename__ = "project"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    project_name: Mapped[str] = mapped_column(String(400), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )

    skill_id: Mapped[UUID] = mapped_column(
        ForeignKey("skill.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    skill: Mapped[Skill] = relationship(back_populates="projects")

    tasks: Mapped[list[Task]] = relationship(
        back_populates="project", cascade="all, delete-orphan", passive_deletes=True
    )

    __table_args__ = (UniqueConstraint("skill_id", "project_name"),)


class Task(Base):
    __tablename__ = "task"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    task_name: Mapped[str] = mapped_column(String(400), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    deadline: Mapped[datetime.datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    project: Mapped[Project] = relationship(back_populates="tasks")

    __table_args__ = (UniqueConstraint("project_id", "task_name"),)
