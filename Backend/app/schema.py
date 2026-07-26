#ruff: noqa

from datetime import datetime
import uuid

from pydantic import BaseModel, EmailStr, Field
from typing import Any

class Token(BaseModel):
    access_token : str
    token_type : str = "bearer"

class UserRequest(BaseModel):
    username : str = Field(min_length=1, max_length=100)
    email : EmailStr = Field(min_length=6, max_length=200)
    password : str = Field(min_length=8, max_length=200)

    def model_post_init(self, context: Any, /) -> None: # pyright: ignore
        super().model_post_init(context)
        self.username = self.username.strip()
        self.email = self.email.lower().strip()
        self.password = self.password.strip()


class SkillCreateRequest(BaseModel):
    name : str
    description : str

    def model_post_init(self, context: Any, /) -> None: # pyright: ignore
        super().model_post_init(context)
        self.name = self.name.strip()
        self.description = self.description.strip()

class SkillIdRequest(BaseModel):
    id : uuid.UUID

class SkillUpdateRequest(SkillCreateRequest):
    id : uuid.UUID



class ProjectsRequest(BaseModel):
    skill_id : uuid.UUID

class ProjectRequest(ProjectsRequest):
    project_id : uuid.UUID

class CreateProject(ProjectsRequest):
    project_name : str
    description : str

    def model_post_init(self, context: Any, /) -> None: # pyright: ignore
        super().model_post_init(context)
        self.project_name = self.project_name.strip()
        self.description = self.description.strip()

class ProjectUpdate(CreateProject, ProjectRequest):
    pass



class TasksRequest(BaseModel):
    skill_id : uuid.UUID
    project_id : uuid.UUID

class TaskRequest(TasksRequest):
    task_id : uuid.UUID

class CreateTask(TasksRequest):
    task_name : str
    description : str
    deadline : datetime

    def model_post_init(self, context: Any, /) -> None: # pyright: ignore
        super().model_post_init(context)
        self.task_name = self.task_name.strip()
        self.description = self.description.strip()

class UpdateTask(CreateTask, TaskRequest):
    pass

class ToggleTaskRequest(TaskRequest):
    toggle : bool