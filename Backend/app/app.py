# External
from fastapi import FastAPI


# Endpoints
from app.endpoints.users import user_router

# Internal


app = FastAPI()
app.include_router(user_router)


