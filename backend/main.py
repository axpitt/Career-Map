import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from config import settings
from logging_config import setup_logging
from middleware.auth import api_key_auth_middleware
from middleware.rate_limit import limiter, ANALYZE_RATE_LIMIT
from services.pdf_service import extract_text_from_pdf
from services.ai_service import analyze_resume
from models.response_models import CareerAnalysisResponse

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CareerMap AI Backend")
    yield
    logger.info("Shutting down CareerMap AI Backend")

# Initialize FastAPI app
app = FastAPI(
    title="CareerMap AI",
    description="AI-powered resume and career analyzer.",
    version="1.0.0",
    lifespan=lifespan,
)

# Add rate limiting
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Custom middleware for API key authentication (if enabled)
if settings.api_key:
    app.middleware("http")(api_key_auth_middleware)


@app.get("/", summary="Health check")
async def root():
    """Health check endpoint."""
    return {
        "message": "CareerMap AI Backend Running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health", summary="Detailed health check")
async def health():
    """Detailed health check with system status."""
    return {
        "status": "healthy",
        "services": {
            "openai": "configured" if settings.openai_api_key else "not_configured",
            "rate_limiting": f"{settings.rate_limit_requests}/{settings.rate_limit_window}s",
            "authentication": "enabled" if settings.api_key else "disabled"
        }
    }


@app.post(
    "/analyze",
    response_model=CareerAnalysisResponse,
    summary="Analyze a resume PDF",
)
@limiter.limit(ANALYZE_RATE_LIMIT)
async def analyze(
    request: Request,
    file: UploadFile = File(..., description="Resume PDF file"),
    city: str = Form(..., description="City where the user is looking for jobs"),
):
    """
    Analyze a resume PDF and provide career insights.

    - **file**: PDF resume file (max 10MB)
    - **city**: User's location for job recommendations
    """
    logger.info(f"Received analysis request from {request.client.host if request.client else 'unknown'}")

    # Input validation
    city = city.strip()
    if not city:
        raise HTTPException(status_code=422, detail="City must not be empty.")

    # Validate file type
    if file.content_type not in settings.allowed_file_types:
        if not (file.filename or "").lower().endswith(".pdf"):
            raise HTTPException(
                status_code=422,
                detail="Only PDF files are accepted. Please upload a valid PDF.",
            )

    try:
        # Step 1: Extract text from PDF
        resume_text = await extract_text_from_pdf(file)

        # Step 2: Send to OpenAI and get analysis
        raw_analysis = analyze_resume(resume_text=resume_text, city=city)

        # Step 3: Validate response with Pydantic model
        validated = CareerAnalysisResponse(**raw_analysis)

        logger.info(f"Successfully completed analysis for city: {city}")
        return validated

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Unexpected error during analysis: {str(exc)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later.",
        )
