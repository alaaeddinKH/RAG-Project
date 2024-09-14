from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    id : Optional[ObjectId] = Field(None, alias="_id")
    chunk_text : str = Field(..., min_lenght=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId

    class Config:   # to allow when take unknown value
        arbitrary_types_allowed = True


        