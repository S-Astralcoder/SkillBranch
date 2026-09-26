from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.endpoints.projects import project_router
from app.endpoints.skills import skill_router
from app.endpoints.tasks import task_router
from app.endpoints.users import user_router

app = FastAPI()



app.include_router(user_router)
app.include_router(skill_router)
app.include_router(project_router)
app.include_router(task_router)

static_dir = Path(__file__).resolve().parent.parent / "static"
app.mount(path="/", app=StaticFiles(directory=str(static_dir), html=True), name="static")
