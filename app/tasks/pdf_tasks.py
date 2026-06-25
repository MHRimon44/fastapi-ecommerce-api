import os
from datetime import datetime

from pypdf import PdfReader


def process_pdf_task(file_path: str) -> None:
    os.makedirs("logs", exist_ok=True)

    try:
        reader = PdfReader(file_path)
        total_pages = len(reader.pages)

        message = (
            f"[{datetime.utcnow()}] PDF PROCESSED\n"
            f"File: {file_path}\n"
            f"Total pages: {total_pages}\n"
            f"{'-' * 50}\n"
        )

    except Exception as error:
        message = (
            f"[{datetime.utcnow()}] PDF PROCESSING FAILED\n"
            f"File: {file_path}\n"
            f"Error: {str(error)}\n"
            f"{'-' * 50}\n"
        )

    with open("logs/pdf_processing.log", "a") as file:
        file.write(message)