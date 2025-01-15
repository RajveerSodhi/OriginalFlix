from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import FastAPI, Query, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel
from database import SessionLocal, engine
from model import OriginalContent, Base


app = FastAPI(
    title="OriginalFlix API",
    version="1.0",
    root_path="/v1",
    docs_url=None,
    description=""",

    Welcome to the OriginalFlix API!

    This API allows users to:
    → Retrieve a catalog of original movies and shows available across multiple streaming platforms.
    → Filter, search, and verify whether a specific title is an original on a particular service.
    → Get the service a title belongs to.

    No authentication required!
    Deployed using Azure Flexible Postgres, Heroku, and Vercel.

    The base URL for all endpoints is www.api.originalflix.dev or api.originalflix.dev.

    Get more information from originalflix.dev.
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
    service: str
    type: str
    language: str
    release_date: date
    genre: str
    status: str
    category: str
    source_id: int

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

def custom_swagger_ui_html(
    *,
    openapi_url: str,
    title: str,
    swagger_js_url: str,
    swagger_css_url: str,
):
    # Original Swagger UI HTML
    swagger_ui_html = get_swagger_ui_html(
        openapi_url=openapi_url,
        title=title,
        swagger_js_url=swagger_js_url,
        swagger_css_url=swagger_css_url,
    )

    # Extract original HTML content
    html_content = swagger_ui_html.body.decode("utf-8")

    # Custom CSS for Swagger UI
    custom_css = """
    <style>
        body, html {
            background-color: #f5f5f4 !important;
            margin: 0;
            overflow-x: hidden;
            padding: 0 0;
            color: #292524;
            font-family: "Readex Pro", sans-serif !important;
        }

        .swagger-ui .title {
            text-indent:-9999px;
            font-family: "Readex Pro", sans-serif !important;
        }

        .swagger-ui .title:before {
            text-indent:0;
            content: "API Docs";
            float:left;
        }

        .swagger-ui .info {
            background-color: none !important;
            margin-left: 80px !important;
            margin-right: 80px !important;
        }

        .swagger-ui .info code {
            padding: 24px 20px !important;
            margin: -24px 0 -12px 0 !important;
            color: #292524 !important;
            font-family: "Readex Pro", sans-serif !important;
            border-radius: 12px !important;
            font-weight: 400 !important;
            font-size: 1rem !important;
        }

        .swagger-ui .info a {
            display: none !important;
        }

        .scheme-container {
            display: none !important;
        }

        .swagger-ui .opblock {
            margin-left: 80px !important;
            margin-right: 80px !important;
            border-radius: 16px !important;
            background-color: white !important;
            padding: 4px 16px !important;
            border: 1px solid #ddd !important;
            box-shadow: 2px 2px 4px 1px #DDDDDD;
            font-family: "Readex Pro", sans-serif !important;
            transition: scale 200ms ease-in-out, box-shadow 200ms ease-in-out;
        }

        .opblock-tag {
            margin-left: 80px !important;
            margin-right: 80px !important;
            border-radius: 16px 16px 0 0 !important;
            margin-bottom: 14px !important;
            outline: none !important;
        }

        .swagger-ui .opblock:hover {
            scale: 1.02;
            box-shadow: 2px 2px 10px 2px #DDDDDD;
        }

        .opblock-summary-method {
            padding: 12px 4px !important;
            border-radius: 8px !important;
            background: linear-gradient(to right, #f86363, #da9030) !important;
            font-family: "Readex Pro", sans-serif !important;
        }

        .opblock-description-wrapper {
            font-size: 1rem !important;
            font-family: "Readex Pro", sans-serif !important;
        }

        .opblock-description-wrapper p {
            font-size: 1rem !important;
            font-family: "Readex Pro", sans-serif !important;
        }

        .opblock-description-wrapper code,
        .opblock-description-wrapper p code {
            color: #f86363 !important;
        }

        .models,
        .models-is-open {
            display: none !important;
        }

        button {
            border-radius: 25px !important;
            padding-top: 10px !important;
            padding-bottom: 10px !important;
            font-family: "Readex Pro", sans-serif !important;
        }

        .example,
        .microlight {
            border-radius: 12px !important;
        }

        footer {
            background-color: #FFFFFF;
            display: flex;
            font-size: 1rem;
            flex_direction: row;
            justify-content: space-around;
            text-align: center;
            padding: 1rem;
            position: relative;
            margin-top: 48px;
            bottom: 0;
            width: 100%;
        }

        .footer-nav {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            width: fit;
        }

        .footer-nav a {
            text-decoration: none;
            color: #292524;
            transition: scale 200ms ease-in-out;
        }

        .footer-nav a:hover {
            scale: 0.9;
            text-decoration: underline;
        }

        main {
            padding: 0 0 !important;
            width: screen;
        }
    </style>
    """

    # Custom Font
    font_html = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@160..700&display=swap" rel="stylesheet">
    """

    # Custom Navbar HTML
    navbar_html = """
    <nav style="background-color: #FFFFFF; color: #292524; padding: 16px; display: flex; justify-content: space-between; align-items: center; width: 100%;">
        <a href="https://originalflix.dev">
            <img src="/logo.png" alt="OriginalFlix Logo" style="height: 3.5rem;">
        </a>
    </nav>
    <main>
    """

    # Custom Footer HTML
    footer_html = """
    </main>
    <footer>
        <div class="footer-nav">
            <a href="https://originalflix.dev"  target="_blank">Home</a>
            <a href="https://api.originalflix.dev" style="margin: 0 20px;">Documentation</a>
            <a href="https://api.originalflix.dev/redoc" style="margin-right: 20px;">Redoc</a>
            <a href="https://buymeacoffee.com/rajveersodhi" target="_blank">Buy me a Coffee</a>
        </div>
        <p>Maintained by <a href="https://rajveersodhi.com" style="text-decoration: none; font-weight: 600; color: #292524;"  target="_blank">Rajveer Sodhi</a></p>
    </footer>
    """

    # Inject navbar and footer into Swagger UI HTML
    modified_html = html_content.replace(
        '<div id="swagger-ui">',
        f'{navbar_html}<div id="swagger-ui">'
    )
    modified_html = modified_html.replace('</body>', f'{footer_html}</body>')
    modified_html = modified_html.replace('</head>', f'{custom_css}{font_html}</head>')

    return HTMLResponse(content=modified_html, media_type="text/html")



# Root Endpoint
@app.get("/", include_in_schema=False)
async def overridden_docs():
    return custom_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

# Redirect to root
@app.get("/docs", include_in_schema=False)
def docs():
    response = RedirectResponse(url='/')
    return response

# Favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("/favicon.ico")

# Logo
@app.get("/logo.png", include_in_schema=False)
async def logo():
    return FileResponse("logo.png")

# get OriginalContent items filtered by service
@app.get("/get-originals", response_model=List[OriginalContentModel], summary="Get Originals by Service", tags=["Endpoints"])
def get_originals(
    service: str = Query(..., description="Filter by the name of the streaming service (case-insensitive)"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve original movies and tv shows for a specific streaming service. The list of available services can be retrieved by running the `/get-available-services` endpoint.

    ### Release Date:
    Dates are formatted as YYYY-MM-DD. For movies and TV shows whose release dates are unavailable, the default date is `2035-01-01`. For TV shows, the release date is set to the date of the premiere of S01E01.
    
    ### Category Column
    OriginalFlix works by scraping several Wikipedia pages regularly to stay up to date about the original content offered by streaming services. You can find more information about this via the About page. The `Category` column of the OriginalFlix database consists of titles given to the various tables present in the Wikipedia page.
    
    Sometimes, the title consists of a broader genre that a piece of content falls under. In that case, it is retained in the category column. For example, for a movie with genre "Investigative Thriller," the category may be "Thriller." In other cases, the category consists of the language of the pieces of content listed in the corresponding table. In this case, OriginalFlix recognizes the language categorization and updates the language column of the database instead, leaving the category entry be "Uncategorized." Rarely, this column might include metadata about the content.

    ### Type:
    There are 4 types that a record can have:
    - `Show`: Original programming
    - `EID Show`: Exclusive International Distribution programming
    - `Movie`: Original films
    - `EID Movie`: Exclusive International Distribution films

    ### Status:
    This column indicates the status assigned to movies and tv shows according to Wikipedia, such as notes on their completion or upcoming additions/seasons.

    ### Source Id:
    The integer listed in this column is the page id of the particular wikipedia article that was scraped to extract a particular record. This has been included for manual verification of the data, if required.

    The Wikipedia article can be retrieved with the listed `source_id` via the URL: `https://en.wikipedia.org/w/index.php?curid=[source_id]`.

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
@app.get("/is-original", summary="Check if Title is an Original", tags=["Endpoints"])
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
@app.get("/get-title-service", summary="Get Service of a Title", tags=["Endpoints"])
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
@app.get("/search-originals", response_model=List[OriginalContentModel], summary="Search Originals Database", tags=["Endpoints"])
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

# get available services
@app.get("/get-available-services", response_model=List[str], summary="Get Available Services", tags=["Endpoints"])
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