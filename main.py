"""AeroFleet Manager - Main Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.api.endpoints import auth, aircraft

# Create tables
Base.metadata.create_all(bind=engine)

# Create app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(aircraft.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "AeroFleet Manager API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
