from fastapi import FastAPI

from app.endpoints.projects import project_router
from app.endpoints.skills import skill_router
from app.endpoints.tasks import task_router
from app.endpoints.users import user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(skill_router)
app.include_router(project_router)
app.include_router(task_router)
