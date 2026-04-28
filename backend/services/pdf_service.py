from fastapi import UploadFile
from utils.file_handler import save_upload_file

class PDFService:
    @staticmethod
    async def process_pdf(file: UploadFile):
        # Save the file
        filename = save_upload_file(file)
        # You could add more logic here (e.g. parsing, database storage)
        return filename

pdf_service = PDFService()
