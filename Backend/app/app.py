# External
from fastapi import FastAPI


# Endpoints
from app.endpoints.users import user_router
from app.endpoints.skills import skill_router
# Internal


app = FastAPI()
app.include_router(user_router)
app.include_router(skill_router)


