from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models import Base

_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/polymind")
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        _engine = create_engine(DATABASE_URL)
    return _engine

def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal

def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

def get_db():
    # Ensure tables exist on first DB access
    init_db()
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


