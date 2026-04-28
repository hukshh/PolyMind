import os
import shutil
from fastapi import UploadFile
from .config import settings
from .logger import logger

def save_upload_file(upload_file: UploadFile) -> str:
    try:
        filename = os.path.basename(upload_file.filename)
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        logger.info(f"Saving file to: {file_path}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        return filename
    except Exception as e:
        logger.error(f"FileHandler Error: Failed to save {upload_file.filename}. Error: {str(e)}")
        raise RuntimeError(f"Could not save file: {str(e)}")
