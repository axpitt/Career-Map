import pdfplumber
import io
import logging
from fastapi import UploadFile, HTTPException
from config import settings

logger = logging.getLogger(__name__)


async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Reads an uploaded PDF file and extracts all text content using pdfplumber.
    Raises HTTPException for invalid or empty PDFs.
    """
    try:
        # Check file size
        file_content = await file.read()
        if len(file_content) > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {settings.max_file_size // (1024*1024)}MB."
            )

        if not file_content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # Validate file type
        if file.content_type not in settings.allowed_file_types:
            if not (file.filename or "").lower().endswith(".pdf"):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid file type. Only PDF files are accepted."
                )

        pdf_stream = io.BytesIO(file_content)

        extracted_text = []

        with pdfplumber.open(pdf_stream) as pdf:
            if len(pdf.pages) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="PDF has no pages."
                )

            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(page_text.strip())

        full_text = "\n\n".join(extracted_text).strip()

        if not full_text:
            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text found in the PDF. "
                    "The file may be scanned or image-based. "
                    "Please upload a text-based PDF."
                ),
            )

        logger.info(f"Successfully extracted {len(full_text)} characters from PDF")
        return full_text

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"PDF processing error: {str(exc)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process PDF file. Please ensure it's a valid PDF.",
        )
