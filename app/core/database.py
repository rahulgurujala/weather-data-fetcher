from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from typing import Generator
from contextlib import contextmanager
from app.config import DATABASE_URL
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Create SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()
metadata = MetaData()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Database session context manager."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        db.close()


def init_db() -> None:
    """Initialize database and create tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
