from fastapi import FastAPI, APIRouter, Depends
from src.helpers.config import get_settings, Settings


base_router = APIRouter(
    prefix="/api/mini", tags=["api"]
)  # this parameter to add words before all of routes and to add tags 

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {"app_name":app_name,
            "app_version": app_version,}
