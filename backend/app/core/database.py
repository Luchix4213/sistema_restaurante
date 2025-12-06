"""
Database configuration and session management
Supports both PostgreSQL (SQLAlchemy) and MongoDB
"""
from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional

# MongoDB imports (optional)
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    from pymongo import MongoClient
except ImportError:
    AsyncIOMotorClient = None
    MongoClient = None

# SQLAlchemy setup for PostgreSQL
if settings.DATABASE_TYPE == "postgresql":
    # Fix for Render/Heroku: Replace postgres:// with postgresql://
    # SQLAlchemy 1.4+ removed support for postgres://
    db_url = settings.DATABASE_URL
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        echo=settings.ENVIRONMENT == "development"
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
else:
    engine = None
    SessionLocal = None
    Base = None

# MongoDB setup
mongodb_client: Optional[AsyncIOMotorClient] = None
mongodb_sync_client: Optional[MongoClient] = None

def get_mongodb():
    """Get MongoDB async client"""
    if AsyncIOMotorClient is None:
        raise ImportError("motor is not installed. Install it with: pip install motor")
    global mongodb_client
    if mongodb_client is None:
        mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    return mongodb_client

def get_mongodb_sync():
    """Get MongoDB sync client"""
    if MongoClient is None:
        raise ImportError("pymongo is not installed. Install it with: pip install pymongo")
    global mongodb_sync_client
    if mongodb_sync_client is None:
        mongodb_sync_client = MongoClient(settings.MONGODB_URL)
    return mongodb_sync_client

def get_db():
    """Dependency for getting database session (PostgreSQL)"""
    if settings.DATABASE_TYPE == "postgresql":
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        # For MongoDB, we use the client directly
        yield get_mongodb()

