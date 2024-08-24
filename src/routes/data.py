from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse  
import os
from src.helpers.config import get_settings, Settings
from src.controllers import DataController
from src.controllers import ProjectControler
import aiofiles
from src.models import ResponseSignal


data_router = APIRouter(
    prefix="/api/mini/data", tags=["api", "data"]
)  # this parameter to add words before all of routes and to add tags 


@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file:UploadFile,
                      app_settings: Settings = Depends(get_settings)):


    # validate the file prop like extension or size
    is_valid, result_signal = DataController().validate_upload_file(file=file)

    if not is_valid:
        return JSONResponse(content={'signal', result_signal})

    project_dir_path = ProjectControler().get_project_path(project_id=project_id)
    file_path = os.path.join(
        project_dir_path,
        file.filename
    )

    async with os.open(file_path, 'wb') as f:
        while chunk := await file.read(app_settings.FILE_DEFULT_CHUNKS_SIZE):
            await f.write(chunk)
    
    return JSONResponse(content={'signal', ResponseSignal.FILE_UPLOAD_SUCCESS.value})
