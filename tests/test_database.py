from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
from database import repository
import pytest

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def test_database_initialization():
    db = TestingSessionLocal()
    scan = repository.create_scan(db, "http://127.0.0.1:8080")
    assert scan.id is not None
    assert scan.target == "http://127.0.0.1:8080"
    db.close()
