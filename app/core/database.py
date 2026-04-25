from pathlib import Path
from dotenv import load_dotenv
import os

# Import the create_engine function to establish database connections
from sqlalchemy import create_engine

# Import sessionmaker to create database session objects for queries
from sqlalchemy.orm import sessionmaker


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
