from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints.projects import project_router
from app.endpoints.skills import skill_router
from app.endpoints.tasks import task_router
from app.endpoints.users import user_router

app = FastAPI()

origins = ["http://127.0.0.1:5500"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


app.include_router(user_router)
app.include_router(skill_router)
app.include_router(project_router)
app.include_router(task_router)
