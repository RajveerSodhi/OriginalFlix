from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import FastAPI, Query, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from database import SessionLocal, engine
from model import OriginalContent, Base


app = FastAPI(
    title="OriginalFlix API",
    version="1.0",
    root_path="/v1",
    description=""",

    Welcome to the OriginalFlix API!

    This API allows users to:
    - Retrieve a catalog of original movies and shows available across multiple streaming platforms.
    - Filter, search, and verify whether a specific title is an original on a particular service.
    - Get the service a title belongs to.

    No authentication required!
    Deployed using Azure Flexible Postgres, Heroku, and Vercel.

    The base URL for all endpoints is www.api.originalflix.dev or api.originalflix.dev
    """
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OriginalContentBase(BaseModel):
    """
    Base model representing the core fields for original content.
    """
    title: str
    type: str
    language: str
    release_date: date
    genre: str
    status: str
    category: str

class OriginalContentModel(OriginalContentBase):
    """
    Model representing original content including its database ID.
    """
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
@app.get("/", summary="Root Endpoint", include_in_schema=False)
def root():
    response = RedirectResponse(url='/docs')
    return response

# get available services
@app.get("/get-available-services", response_model=List[str], summary="Get Available Services")
def get_services(db: Session = Depends(get_db)):
    """
    Retrieve all unique streaming services available in the database. Use this generated list to get the valid services you can filter with in other endpoints.

    ### Response:
    - A list of streaming services (e.g., Netflix, Hulu, Amazon Prime).

    ### Example Request:
    `GET https://api.originalflix.dev/get-available-services`
    """
    services = db.query(OriginalContent.service).distinct().all()
    return [service for service, in services]

# get OriginalContent items filtered by service
@app.get("/get-originals", response_model=List[OriginalContentModel], summary="Get Originals by Service")
def get_originals(
    service: str = Query(..., description="Filter by the name of the streaming service (case-insensitive)"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve original movies and tv shows for a specific streaming service. The list of available services can be retrieved by running the `/get-available-services` endpoint.

    ### Release Dates
    Dates are formatted as YYYY-MM-DD. For movies and TV shows whose release dates are unavailable, the default date is `2035-01-01`. For TV shows, the release date is set to the date of the premiere of S01E01.
    
    ### Response:
    A list of original content items (movies/shows) belonging to the specified service.

    ### Example Request:
    `GET https://api.originalflix.dev/get-originals?service=Netflix&skip=0&limit=5`
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
@app.get("/is-original", summary="Check if Title is an Original")
def is_original(
    title: str = Query(..., description="Title of the movie/show to check"),
    service: str = Query(..., description="Streaming service directory to check in"),
    db: Session = Depends(get_db)
):
    """
    Checks if a given title is an original for a given service.

    ### Response:
    JSON object with:
    - `title`: The queried title.
    - `service`: The queried service.
    - `exists`: Boolean indicating whether the title exists as an original.

    ### Example Request:
    `GET https://api.originalflix.dev/is-original?title=Stranger%20Things&service=Netflix`
    """
    query = db.query(OriginalContent)

    query = query.filter(OriginalContent.title.ilike(title))  
    
    if service:
        query = query.filter(OriginalContent.service.ilike(service))
    
    exists = bool(query.first())
    return {"title": title, "service": service, "exists": exists}

# get the service of an given title
@app.get("/get-title-service", summary="Get Service of a Title")
def get_service(
    title: str = Query(..., description = "Title of the movie/show to find the service for"),
    db: Session = Depends(get_db)
):
    """
    Returns the streaming service where a specified title is available if it exists in the database.
    
    ### Response:
    JSON object with:
    - `service`: Name of the streaming service where the title is available.

    ### Example Request:
    `GET https://api.originalflix.dev/get-title-service?title=The%20Crown`
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
@app.get("/search-originals", response_model=List[OriginalContentModel], summary="Search Originals Database")
def search_originals(
    title: Optional[str]= Query(None, description = "Search by title (partial match)"),
    service: Optional[str] = Query(None, description = "Filter by streaming service"),
    type: Optional[str] = Query(None, description = "Filter by type - 'Movie' or 'Show'"),
    language: Optional[str] = Query(None, description = "Filter by language"),
    status: Optional[str] = Query(None, description = "Filter by status"),
    category: Optional[str] = Query(None, description = "Filter by category"),
    genre: Optional[str] = Query(None, description = "Filter by genre"),
    release_date: Optional[date] = Query(None, description = "Filter by exact release date (YYYY-MM-DD)"),
    min_release_date: Optional[date] = Query(None, description = "Filter content to release date uptil this date (YYYY-MM-DD)"),
    max_release_date: Optional[date] = Query(None, description = "Filter content to release date after this date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Allows flexible searching for original movies and tv shows across columns in the database. Filtering is based on "is like" comparisons.

    ### About the Category Column:
    OriginalFlix works by scraping several Wikipedia pages regularly to stay up to date about the original content offered by streaming services. You can find more information about this via the About page. The `Category` column of the OriginalFlix database consists of titles given to the various tables present in the Wikipedia page.
    
    Sometimes, the title consists of a broader genre that a piece of content falls under. In that case, it is retained in the category column. For example, for a movie with genre "Investigative Thriller," the category may be "Thriller." In other cases, the category consists of the language of the pieces of content listed in the corresponding table. In this case, OriginalFlix recognizes the language categorization and updates the language column of the database instead, leaving the category entry be "Uncategorized." Rarely, this column might include metadata about the content.

    ### Response:
    A list of original content items matching the search criteria.

    ### Example Request:
    `GET https://api.originalflix.dev/search-originals?title=the&service=Netflix&genre=Drama&min_release_date=2015-01-01&max_release_date=2020-12-31&limit=10`
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