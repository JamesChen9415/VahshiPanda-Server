import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MONGODBDB_HOST = os.environ.get("MONGODBDB_HOST", "localhost")
MONGODBDB_USERNAME = os.environ.get("MONGODBDB_USERNAME", "postgres")
MONGODBDB_PASSWORD = os.environ.get("MONGODBDB_PASSWORD", "postgres")
MONGODBDB_PORT = os.environ.get("MONGODBDB_PORT", "5432")

SQLALCHEMY_DATABASE_URL = f"postgresql://{MONGODBDB_USERNAME}:{MONGODBDB_PASSWORD}@{MONGODBDB_HOST}:{MONGODBDB_PORT}/vashipanda_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency for external
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
