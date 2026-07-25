from fastapi import APIRouter


project_router = APIRouter(prefix="/project", tags=["Project"])


async def get_all_projects():
    pass

async def get_project():
    pass

async def create_project():
    pass

async def update_project():
    pass

async def delete_project():
    pass