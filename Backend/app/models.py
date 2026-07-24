from __future__ import annotations

import datetime
from uuid import UUID
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id : Mapped[UUID] = mapped_column(Integer, primary_key=True)
    username : Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String(200), nullable=False)
    
    created_at : Mapped[Date] = mapped_column(Date, default=datetime.date, nullable=False)

    skills : Mapped[list[Skill]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = "skill"

    id : Mapped[UUID] = mapped_column(Integer, primary_key=True)
    skill_name : Mapped[str] = mapped_column(String(400), nullable=False)
    description : Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at : Mapped[Date] = mapped_column(Date, default=datetime.date, nullable=False)
    updated_at : Mapped[Date] = mapped_column(Date, default=datetime.date, nullable=False)

    user_id : Mapped[UUID] = mapped_column(ForeignKey("user.id"))

    user : Mapped[User] = relationship(back_populates="skills")

    projects : Mapped[list[Project]] = relationship(back_populates="skill")

class Project(Base):
    __tablename__ = "project"

    id : Mapped[UUID] = mapped_column(Integer, primary_key=True)
    project_name : Mapped[str] = mapped_column(String(400), nullable=False)
    description : Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at : Mapped[Date] = mapped_column(Date, default=datetime.date, nullable=False)
    updated_at : Mapped[Date] = mapped_column(Date, default=datetime.date, nullable=False)

    skill_id : Mapped[UUID] = mapped_column(ForeignKey("skill.id"))

    skill : Mapped[Skill] = relationship(back_populates="projects")

    tasks : Mapped[list[Task]] = relationship(back_populates="project")


class Task(Base):
    __tablename__ = "task"
    id : Mapped[UUID] = mapped_column(Integer, primary_key=True)
    task_name : Mapped[str] = mapped_column(String(400), nullable=False)
    completed : Mapped[bool] = mapped_column(Boolean, nullable=False)

    deadline : Mapped[DateTime] = mapped_column(DateTime)
    created_at : Mapped[Date] = mapped_column(Date, default=datetime.date, nullable=False)
    updated_at : Mapped[Date] = mapped_column(Date, default=datetime.date, nullable=False)

    project_id : Mapped[UUID] = mapped_column(ForeignKey("project.id"))

    project : Mapped[Project] = relationship(back_populates="tasks")




