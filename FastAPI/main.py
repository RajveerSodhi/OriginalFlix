from datetime import date
from fastapi import FastAPI, Query, HTTPException, status, Depends
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


# db_dependency = Annotated[Session, Depends(get_db)]

Base.metadata.create_all(bind=engine)


# Root endpoint
@app.get("/", summary="Root Endpoint")
def root():
    return {"message": "Welcome to the OriginalFlix API! Check originalflix.dev for more info."}

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
    service: str = Query(..., description="Filter by service"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Returns a list of movie/show items for a given 'service'.
    Paginated by skip & limit.
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
    service: Optional[str] = Query(None, description="Optional service to filter by"),
    db: Session = Depends(get_db)
):
    """
    Checks if a record with 'title' (and optionally 'service') exists in the DB.
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
    title: Optional[str] = None,
    service: Optional[str] = None,
    type: Optional[str] = None,
    language: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    genre: Optional[str] = None,
    release_date: Optional[date] = None,
    min_release_date: Optional[date] = None,
    max_release_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Allows flexible searching across columns. 
    Example usage:
        /search-originals?title=heist&service=netflix&language=english
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