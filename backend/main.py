from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import FastAPI, Query, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import SessionLocal, engine
from model import OriginalContent, Base


app = FastAPI(title="OriginalFlix API", version="1.0")

origins = [
    "*",
    "https://www.api.originalflix.dev",
    "https://api.originalflix.dev",
    "http://localhost:8000",
]

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

Base.metadata.create_all(bind=engine)


# Root endpoint
@app.get("/", summary="Root Endpoint")
def root():
    return {"message": "Welcome to the OriginalFlix API! Check api.originalflix.dev/docs for more info."}

# Handle favicon requests
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {"message": "No favicon available"}

# get available services
@app.get("/get-services", response_model=List[str])
def get_services(db: Session = Depends(get_db)):
    """
    Returns a list of unique services available in the database.
    """
    services = db.query(OriginalContent.service).distinct().all()
    return [service for service, in services]

# get OriginalContent items filtered by service
@app.get("/get-originals", response_model=List[OriginalContentModel])
def get_originals(
    service: str = Query(..., description="Filter by streaming service"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Returns a list of movie/show items for a given streaming service.
    The list of available services can be retrieved by running the /get-services endpoint.
    """

    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="skip cannot be negative."
        )
    if limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit must be positive."
        )

    query = db.query(OriginalContent)
    if service:
        query = query.filter(OriginalContent.service.ilike(service))
    
    originals = query.offset(skip).limit(limit).all()
    return originals

# check if a given title is an original for a given service
@app.get("/is-original")
def is_original(
    title: str = Query(..., description="Title of the movie/show to check"),
    service: str = Query(..., description="Streaming service directory to check in"),
    db: Session = Depends(get_db)
):
    """
    Checks if a given title is an original for a given service.
    Returns a JSON { 'title': ..., 'service': ..., 'exists': True/False }
    """
    query = db.query(OriginalContent)

    query = query.filter(OriginalContent.title.ilike(title))  
    
    if service:
        query = query.filter(OriginalContent.service.ilike(service))
    
    exists = bool(query.first())
    return {"title": title, "service": service, "exists": exists}

# get the service of an given title
@app.get("/get-service")
def get_service(
    title: str = Query(..., description = "Title of the movie/show to find"),
    db: Session = Depends(get_db)
):
    """
    Returns the service of a given title if it exists in the database.
    Returns a JSON { 'service': ... }
    """
    if not title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title parameter cannot be empty."
        )

    query = db.query(OriginalContent)

    query = query.filter(OriginalContent.title.ilike(title))

    result = query.first()
    service = None

    if result:
        service = result.service
        return {"service": service}
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"No record found for title '{title}'."
        )


# search for OriginalContent items
@app.get("/search-originals", response_model=List[OriginalContentModel])
def search_originals(
    title: Optional[str]= Query(None, description = "Filter by title"),
    service: Optional[str] = Query(None, description = "Filter by streaming service"),
    type: Optional[str] = Query(None, description = "Filter by 'Movie' or 'Show'"),
    language: Optional[str] = Query(None, description = "Filter by language"),
    status: Optional[str] = Query(None, description = "Filter by status"),
    category: Optional[str] = Query(None, description = "Filter by category"),
    genre: Optional[str] = Query(None, description = "Filter by genre"),
    release_date: Optional[date] = Query(None, description = "Filter by release date"),
    min_release_date: Optional[date] = Query(None, description = "Filter content to release date uptil this date"),
    max_release_date: Optional[date] = Query(None, description = "Filter content to release date after this date"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Allows flexible searching across columns in the database. Filtering is based on "is like" comparisons.
    """

    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="skip cannot be negative."
        )
    if limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit must be positive."
        )

    if min_release_date and max_release_date and min_release_date > max_release_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_release_date cannot be greater than max_release_date."
        )

    query = db.query(OriginalContent)

    if title:
        query = query.filter(OriginalContent.title.ilike(f"%{title}%"))
    if service:
        query = query.filter(OriginalContent.service.ilike(service))
    if type:
        query = query.filter(OriginalContent.type.ilike(type))
    if language:
        query = query.filter(OriginalContent.language.ilike(language))
    if status:
        query = query.filter(OriginalContent.status.ilike(status))
    if category:
        query = query.filter(OriginalContent.category.ilike(category))
    if genre:
        query = query.filter(OriginalContent.genre.ilike(genre))
    if release_date:
        query = query.filter(OriginalContent.release_date == release_date)
    if min_release_date:
        query = query.filter(OriginalContent.release_date >= min_release_date)
    if max_release_date:
        query = query.filter(OriginalContent.release_date <= max_release_date)

    results = query.offset(skip).limit(limit).all()
    return results

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred. Please try again later."},
    )