from fastapi import UploadFile
from ..utils.file_handler import save_upload_file
from ..utils.logger import logger

class PDFService:
    @staticmethod
    async def process_pdf(file: UploadFile):
        logger.info(f"PDFService: Processing file {file.filename}")
        try:
            filename = save_upload_file(file)
            return filename
        except Exception as e:
            logger.error(f"PDFService Error: {str(e)}")
            raise e

pdf_service = PDFService()
