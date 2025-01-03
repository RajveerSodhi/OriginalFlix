from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your existing code
import wiki_content
from process_content import extract_tables, process_table
from model import OriginalContent, Base
from database import DATABASE_URL

# 1) Create engine & session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def update_database():
    """
    Fetches all relevant Wikipedia pages for original content,
    extracts & processes each table, then inserts unique rows
    into the 'OriginalContent' table in PostgreSQL.
    """

    # 2) Define all the wiki functions you want to call
    wiki_functions = [
        [
            wiki_content.return_NF_programming,
            wiki_content.return_NF_ended_programming,
            wiki_content.return_NF_exclusive_intl_distribution_programming
        ],
        [
            wiki_content.return_NF_standup_specials,
            wiki_content.return_NF_exclusive_intl_distribution_films,
            wiki_content.return_NF_films_2015_to_2017,
            wiki_content.return_NF_films_2018,
            wiki_content.return_NF_films_2019,
            wiki_content.return_NF_films_2020,
            wiki_content.return_NF_films_2021,
            wiki_content.return_NF_films_2022,
            wiki_content.return_NF_films_2023,
            wiki_content.return_NF_films_2024,
            wiki_content.return_NF_films_since_2025
        ],
        wiki_content.return_APV_programming,
        wiki_content.return_APV_ended_programming,
        wiki_content.return_APV_films,
        wiki_content.return_APV_exclusive_intl_distribution_programming,
        wiki_content.return_ATVP_programming,
        wiki_content.return_ATVP_films,
        wiki_content.return_DP_programming,
        wiki_content.return_DP_films,
        wiki_content.return_ST_programming,
        wiki_content.return_HL_programming,
        wiki_content.return_HL_films,
        wiki_content.return_HL_exclusive_intl_distribution_programming,
        wiki_content.return_Z5_programming,
        wiki_content.return_Z5_films,
        wiki_content.return_PC_programming,
        wiki_content.return_PMP_programming,
        wiki_content.return_PMP_films,
        wiki_content.return_MAX_programming,
        wiki_content.return_MAX_exclusive_intl_distribution_programming,
        wiki_content.return_HS_programming,
        wiki_content.return_HS_films,
    ]

    # 3) Create the table(s) if they don't already exist
    Base.metadata.create_all(bind=engine)

    # 4) Initialize DB session
    db: Session = SessionLocal()

    # 5) Iterate over each wiki function to fetch & process data
    for fn in wiki_functions:
        html_content = fn()  # e.g., wiki_content.return_NF_films_2018()
        
        # Extract all tables from this HTML
        tables = extract_tables(html_content)

        for table_data in tables:
            cleaned_table = process_table(table_data)
            if not cleaned_table:
                continue
            
            # Each cleaned_table has `headers` and `rows`
            # Example of final_headers: ["Title", "Release_year", "Genre", "Language", "Status"]
            # cleaned_table["rows"] might look like [[title, "2025-01-01", "Action", "English", "Active"], ...]
            
            # 6) Insert each row while checking for duplicates
            for row in cleaned_table["rows"]:
                # row[0] => title
                title = row[0]
                
                # Check for existing record by `title` (or however you define "duplicate")
                existing = db.query(OriginalContent).filter_by(title=title).first()
                if existing:
                    continue  # Skip duplicates

                # Otherwise, create a new OriginalContent entry
                # Adjust indices to match your final_headers
                # Let's assume your process_table sets columns in this order:
                # [Title, Release_year, Genre, Language, Status]
                # and you want to fill your DB model with them:
                release_year = row[1]     # e.g., "2025-01-01" or just year?
                genre = row[2]
                language = row[3]
                status = row[4]

                # Convert release_year to a date if needed, or store as string
                # Here we assume your DB model has 'release_date' as a Date
                # If row[1] is "2025-08-10", parse it or store partial if needed
                # For demonstration, let's assume it's "YYYY-MM-DD"
                from datetime import datetime
                parsed_date = None
                if release_year:
                    try:
                        parsed_date = datetime.strptime(release_year, "%Y-%m-%d")
                    except ValueError:
                        # handle partial or invalid date
                        pass

                new_entry = OriginalContent(
                    title=title,
                    type="Unknown",      # or from the table if you have that in your data
                    service="Unknown",   # or set it based on your function, e.g., "Netflix" / "Amazon" 
                    language=language,
                    release_date=parsed_date,
                    genre=genre,
                    status=status
                )
                
                db.add(new_entry)

    # 7) Commit all changes
    db.commit()
    db.close()

    print("Database updated successfully!")