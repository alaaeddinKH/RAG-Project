from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File_validated_successfuly"
    FILE_TYPE_NOT_SUPPORTED = "File_type_not_supported"
    FILE_SIZE_NOT_SUPPORTED = "File_size_not_supported"
    FILE_UPLOAD_SUCCESS = "File_upload_Success"
    FILE_UPLOAD_FAILED = "File_upload_failed"