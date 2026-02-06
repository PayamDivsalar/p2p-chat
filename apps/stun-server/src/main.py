"""
STUN Server - Peer Address Management Server
Main entry point for the application
"""

from fastapi import FastAPI
import uvicorn
import logging
from contextlib import asynccontextmanager

from .core.config import get_settings
from .core.redis_client import get_redis_client
from .api.endpoints import peers_router, health_router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting STUN server...")
    redis_client = get_redis_client()
    try:
        redis_client.connect()
        logger.info("Successfully connected to Redis")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down STUN server...")
    redis_client.disconnect()
    logger.info("Server shutdown complete")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        description="Peer address management server for P2P chat system",
        version=settings.app_version,
        lifespan=lifespan
    )
    
    # Include routers
    app.include_router(health_router)
    app.include_router(peers_router)
    
    return app


# Create application instance
app = create_app()


def main() -> None:
    """Run STUN server"""
    settings = get_settings()
    
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )


if __name__ == "__main__":
    main()
