from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse  
import os
from src.helpers.config import get_settings, Settings
from src.controllers import ProjectControler, ProcessController, DataController
import aiofiles
from src.models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from src.models.projectModel import ProjectModel
from src.models.ChunkModel import ChunkModel
from src.models.db_schemes.data_chunks import DataChunk

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/mini/data", tags=["api", "data"]
)  # this parameter to add words before all of routes and to add tags 


@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file:UploadFile,
                      app_settings: Settings = Depends(get_settings)):


    project_model = ProjectModel(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(project_id=project_id)
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

    return JSONResponse(content={
        'signal': ResponseSignal.FILE_UPLOAD_SUCCESS.value,
        'file_id': file_id,
        
       })


@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = ProjectModel(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(project_id=project_id)

    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id)
    chunks = process_controller.proccess_file_content(
        file_id=file_id, 
        file_content=file_content,
        chunk_size=chunk_size,
        chunk_overlap=overlap_size)
    
    if chunks is None or len(chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.PROCESSING_FAILED.value
            }
        )
    
    file_chunks_records = [
        DataChunk(
           chunk_text = chunk.page_content , 
           chunk_metadata = chunk.metadata,
           chunk_order = i+1 ,
           chunk_project_id = project.id ,    
        )
        for i, chunk in enumerate(chunks)

    ]
    chunk_model = ChunkModel(
        db_client=request.app.db_client
    )

    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

    no_records = await chunk_model.insert_many_chunks(chunks = file_chunks_records)

    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records
        }
    )

