from fastapi import FastAPI, APIRouter
import os

base_router = APIRouter(
    prefix="/api/mini", tags=["api"]
)  # this parameter to add words before all of routes and to add tags 

@base_router.get("/")
async def welcome():
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')
    return {"app_name":app_name,
            "app_version": app_version,}
