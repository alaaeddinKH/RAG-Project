from src.helpers.config import get_settings, Settings
import os 
import random
import string

class BaseController:
    
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir = os.path.join(
            self.base_dir,
            "asset/files"
        )

    def generate_random_string(self, lenght: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=lenght))