from src.helpers.config import get_settings

class BaseDataModel():

    def __init__(self, db_client: object):
        self.db_client = db_client
        self.app_setting = get_settings()
        