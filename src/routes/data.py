from fastapi import FastAPI, APIRouter, Depends, UploadFile
import os
from src.helpers.config import get_settings, Settings
from src.controllers import DataController


data_router = APIRouter(
    prefix="/api/mini/data", tags=["api", "data"]
)  # this parameter to add words before all of routes and to add tags 


@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file:UploadFile,
                      app_settings: Settings = Depends(get_settings)):


    # validate the file prop like extension or size
    is_valid = DataController().validate_upload_file(file=file)

    return is_valid