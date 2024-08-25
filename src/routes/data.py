from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse  
import os
from src.helpers.config import get_settings, Settings
from src.controllers import DataController
from src.controllers import ProjectControler
import aiofiles
from src.models import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/mini/data", tags=["api", "data"]
)  # this parameter to add words before all of routes and to add tags 


@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file:UploadFile,
                      app_settings: Settings = Depends(get_settings)):


    # validate the file prop like extension or size
    is_valid, result_signal = DataController().validate_upload_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    project_dir_path = ProjectControler().get_project_path(project_id=project_id)
    file_path, file_id = DataController().generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFULT_CHUNKS_SIZE):
                await f.write(chunk)

    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(content={'signal': ResponseSignal.FILE_UPLOAD_SUCCESS.value})
