from .BaseController import BaseController
from fastapi import UploadFile
from src.models import ResponseSignal
import os

class ProjectControler(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str):
        project_dir = os.path.join(
            self.file_dir,
            project_id
        )

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        
        return project_dir