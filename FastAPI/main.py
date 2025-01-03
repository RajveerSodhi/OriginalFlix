from datetime import date
from fastapi import FastAPI, Query, HTTPException, Depends
from typing import List, Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from model import OriginalContent, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OriginalFlix API", version="1.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OriginalContentBase(BaseModel):
    title: str
    type: str
    language: str
    release_date: date
    genre: str

class OriginalContentModel(OriginalContentBase):
    id: int

    class Config:
        from_attributes = True


# get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

Base.metadata.create_all(bind=engine)


# Root endpoint
@app.get("/", summary="Root Endpoint")
def root():
    return {"message": "Welcome to the OriginalFlix API!"}

# get List of Originals
@app.get("/originals", response_model=List[OriginalContentModel], summary="Get List of Originals")
async def read_netflix_originals(db: db_dependency, skip: int = 0, limit: int = 100):
    originals = db.query(OriginalContent).offset(skip).limit(limit).all()
    return originals


# Check if a title exists in the database
@app.get("/check-title/", summary="Check Title in Originals")
def check_title(title: str = Query(..., description="Title of the program to check")):
    db = SessionLocal()
    try:
        # Query the database to see if the title exists
        result = db.query(OriginalContent).filter(OriginalContent.title.ilike(title)).first()
        exists = bool(result)
        return {"title": title, "exists": exists}
    finally:
        db.close()