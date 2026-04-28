import os
import shutil
from fastapi import UploadFile
from .config import settings

def save_upload_file(upload_file: UploadFile) -> str:
    file_path = os.path.join(settings.UPLOAD_DIR, upload_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return upload_file.filename
