import uuid

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token : str
    token_type : str = "bearer"

class UserRequest(BaseModel):
    username : str = Field(min_length=1, max_length=100)
    email : EmailStr
    password : str = Field(min_length=8, max_length=200)

class SkillCreateRequest(BaseModel):
    name : str
    description : str

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

class ProjectUpdate(CreateProject, ProjectRequest):
    pass


