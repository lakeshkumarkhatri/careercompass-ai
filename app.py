import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from api.health import router as health_router
from api.resume import router as resume_router
from api.jobs import router as jobs_router
from api.advisor import router as advisor_router
from api.roadmap import router as roadmap_router
from api.interview import router as interview_router
from api.report import router as report_router
from api.profile import router as profile_router
from core.logging import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("Starting up CareerCompass AI")
    yield
    logger.info("Shutting down CareerCompass AI")

# Create FastAPI app
app = FastAPI(title="CareerCompass AI", lifespan=lifespan)

# Middleware for request lifecycle logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Started {request.method} {request.url}")
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(f"Completed {request.method} {request.url} in {duration:.2f}s with status {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error handling request {request.method} {request.url}: {e}")
        raise

# Include routers
app.include_router(health_router, prefix="/api")
app.include_router(resume_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")
app.include_router(advisor_router, prefix="/api")
app.include_router(roadmap_router, prefix="/api")
app.include_router(interview_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(profile_router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to CareerCompass AI"}
