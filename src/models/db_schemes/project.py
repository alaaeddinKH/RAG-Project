from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id : Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @validator("project_id")
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("project id must be alphanumaric")
        
        return value


    class Config:   # to allow when take unknown value
        arbitrary_types_allowed = True


        