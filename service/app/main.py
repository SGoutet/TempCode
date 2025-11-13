"""
Main FastAPI application.
"""
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking Service API",
    description="REST service for bank user management",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)


@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns:
        Welcome message.
    """
    return {"message": "Banking Service API"}


@app.get("/health")
async def health():
    """
    Health check endpoint.
    
    Returns:
        Health status.
    """
    return {"status": "healthy"}

