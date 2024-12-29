from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional

# Database URL
DATABASE_URL = "postgresql://postgres:root@localhost:5433/netflix-originals"

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the database model
class NetflixOriginal(Base):
    __tablename__ = "netflix_originals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    language = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    genre = Column(String, nullable=True)

# Ensure the table exists
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Netflix Originals API", description="Check if a title is a Netflix Original", version="1.0")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/", summary="Root Endpoint")
def root():
    return {"message": "Welcome to the Netflix Originals API!"}

# Root API endpoint
@app.get("/api/", summary="Root Endpoint")
def root():
    return {"message": "Welcome to the Netflix Originals API!"}

# Check if a title exists in the database
@app.get("/api/check-title/", summary="Check Title in Netflix Originals")
def check_title(title: str = Query(..., description="Title of the program to check")):
    db = SessionLocal()
    try:
        # Query the database to see if the title exists
        result = db.query(NetflixOriginal).filter(NetflixOriginal.title.ilike(title)).first()
        exists = bool(result)
        return {"title": title, "exists": exists}
    finally:
        db.close()