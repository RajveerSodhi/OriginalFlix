from datetime import date
from fastapi import FastAPI, Query, HTTPException, Depends
from typing import List, Annotated, Optional
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


# @app.get("/get-originals", response_model=List[OriginalContentModel])
# async def get_originals(
#     service: Optional[str] = Query(None, description="Filter by service (e.g. Netflix, Hulu)"),
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = db_dependency
# ):
#     """
#     Returns a list of OriginalContent items, optionally filtered by 'service'.
#     Paginated by skip & limit.
#     """
#     query = db.query(OriginalContent)
#     if service:
#         query = query.filter(OriginalContent.service.ilike(service))
    
#     originals = query.offset(skip).limit(limit).all()
#     return originals


# @app.get("/check-original")
# def check_original(
#     title: str = Query(..., description="Title of the program to check"),
#     service: Optional[str] = Query(None, description="Optional service to filter by"),
#     db: Session = db_dependency
# ):
#     """
#     Checks if a record with 'title' (and optionally 'service') exists in the DB.
#     Returns a JSON { 'title': ..., 'service': ..., 'exists': True/False }
#     """
#     query = db.query(OriginalContent)

#     # match title case-insensitively
#     query = query.filter(OriginalContent.title.ilike(title))  
    
#     if service:
#         query = query.filter(OriginalContent.service.ilike(service))
    
#     exists = bool(query.first())
#     return {"title": title, "service": service, "exists": exists}


# @app.get("/search-originals", response_model=List[OriginalContentModel])
# def search_originals(
#     # Query parameters for each column, all optional
#     title: Optional[str] = None,
#     service: Optional[str] = None,
#     type: Optional[str] = None,
#     language: Optional[str] = None,
#     status: Optional[str] = None,
#     category: Optional[str] = None,
#     genre: Optional[str] = None,
#     # For example, release_date could also be filtered with min/max if needed
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = db_dependency
# ):
#     """
#     Allows flexible searching across columns. 
#     Example usage:
#         /search-originals?title=heist&service=netflix&language=english
#     """
#     query = db.query(OriginalContent)

#     if title:
#         # partial match for title (contains)
#         query = query.filter(OriginalContent.title.ilike(f"%{title}%"))
#     if service:
#         query = query.filter(OriginalContent.service.ilike(service))
#     if type:
#         query = query.filter(OriginalContent.type.ilike(type))
#     if language:
#         query = query.filter(OriginalContent.language.ilike(language))
#     if status:
#         query = query.filter(OriginalContent.status.ilike(status))
#     if category:
#         query = query.filter(OriginalContent.category.ilike(category))
#     if genre:
#         query = query.filter(OriginalContent.genre.ilike(genre))

#     # You could add more advanced date filters as well if desired

#     results = query.offset(skip).limit(limit).all()
#     return results