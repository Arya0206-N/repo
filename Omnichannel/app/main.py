from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router
from app.core.logging import configure_logging
from app.db.session import SessionLocal
from app.db.init_db import init_db

app = FastAPI(title=settings.PROJECT_NAME)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Initialize database
@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    init_db(db)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Configure logging
configure_logging()