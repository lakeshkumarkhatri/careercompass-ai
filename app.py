from fastapi import FastAPI
from api.health import router as health_router
from core.logging import setup_logging
import logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="CareerCompass AI")

# Include routers
app.include_router(health_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Startup tasks."""
    logger.info("Starting up CareerCompass AI")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to CareerCompass AI"}
