from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Import your existing code
import wiki_content
from process_content import extract_tables, process_table
from model import OriginalContent, Base
from database import DATABASE_URL

# Create engine & session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def update_database():

    # Define all the wiki functions you want to call
    wiki_functions = [
        # Netflix
        [
            # Programming
            [
                wiki_content.return_NF_programming,
                wiki_content.return_NF_ended_programming
            ],
            # Exclusive International Distribution Programming
            [
                wiki_content.return_NF_exclusive_intl_distribution_programming
            ],
            # Films
            [
                wiki_content.return_NF_standup_specials,
                wiki_content.return_NF_films_2015_to_2017,
                wiki_content.return_NF_films_2018,
                wiki_content.return_NF_films_2019,
                wiki_content.return_NF_films_2020,
                wiki_content.return_NF_films_2021,
                wiki_content.return_NF_films_2022,
                # wiki_content.return_NF_films_2023,
                wiki_content.return_NF_films_2024,
                wiki_content.return_NF_films_since_2025
            ],
            # Exclusive International Distribution Films
            [
                wiki_content.return_NF_exclusive_intl_distribution_films
            ]
        ],
        # Amazon Prime Video
        [
            # Programming
            [
            wiki_content.return_APV_programming,
            wiki_content.return_APV_ended_programming,
            ],
            # Exclusive International Distribution Programming
            [
                wiki_content.return_APV_exclusive_intl_distribution_programming
            ],
            # Films
            [
            wiki_content.return_APV_films
            ],
            # Exclusive International Distribution Films
            []
        ],
        # Apple TV+
        [
            # Programming
            [
                wiki_content.return_ATVP_programming
            ],
            # Exclusive International Distribution Programming
            [],
            # Films
            [
                wiki_content.return_ATVP_films
            ],
            # Exclusive International Distribution Films
            []
        ],
        # Disney+
        [
            # Programming
            [
                wiki_content.return_DP_programming
            ],
            # Exclusive International Distribution Programming
            [],
            # Films
            [
                wiki_content.return_DP_films
            ],
            # Exclusive International Distribution Films
            []
        ],
        # Star
        [
            # Programming
            [
                wiki_content.return_ST_programming
            ],
            # Exclusive International Distribution Programming
            [],
            # Films
            [],
            # Exclusive International Distribution Films
            []
        ],
        # Hulu
        [
            # Programming
            [
                wiki_content.return_HL_programming
            ],
            # Exclusive International Distribution Programming
            [
                wiki_content.return_HL_exclusive_intl_distribution_programming
            ],
            # Films
            [
                wiki_content.return_HL_films
            ],
            # Exclusive International Distribution Films
            []
        ],
        # Zee5
        [
            # Programming
            [
                wiki_content.return_Z5_programming
            ],
            # Exclusive International Distribution Programming
            [],
            # Films
            [
                # wiki_content.return_Z5_films
            ],
            # Exclusive International Distribution Films
            []
        ],
        # Peacock
        [
            # Programming
            [
                wiki_content.return_PC_programming
            ],
            # Exclusive International Distribution Programming
            [],
            # Films
            [],
            # Exclusive International Distribution Films
            []
        ],
        # Paramount+
        [
            # Programming
            [
                wiki_content.return_PMP_programming
            ],
            # Exclusive International Distribution Programming
            [],
            # Films
            [
                wiki_content.return_PMP_films
            ],
            # Exclusive International Distribution Films
            []
        ],
        # Max
        [
            # Programming
            [
                wiki_content.return_MAX_programming,
            ],
            # Exclusive International Distribution Programming
            [
                wiki_content.return_MAX_exclusive_intl_distribution_programming
            ],
            # Films
            [],
            # Exclusive International Distribution Films
            []
        ],
        # Hotstar
        [
            # Programming
            [
                wiki_content.return_HS_programming
            ],
            # Exclusive International Distribution Programming
            [],
            # Films
            [
                wiki_content.return_HS_films
            ],
            # Exclusive International Distribution Films
            []
        ]
    ]

    # Create the table
    Base.metadata.create_all(bind=engine)

    # Initialize DB session
    db: Session = SessionLocal()

    # Iterate over each wiki function to fetch & process data
    services = ["Netflix", "Amazon Prime Video", "Apple TV+", "Disney+", "Star", "Hulu", "Zee5", "Peacock", "Paramount+", "Max", "Hotstar"]
    for service in wiki_functions:
        current_service = services.pop(0)
        types = ["Show", "EID Show", "Movie", "EID Movie"]

        print(f"Updating {current_service} original content...")

        for type in service:
            current_type = types.pop(0)

            print(f"Fetching {current_type} data...")

            for fn in type:

                print(f"Processing function {fn.__name__}...")

                fn_result = fn()
                html_content = fn_result[0]
                source_id = fn_result[1]
        
                # Extract all tables from this HTML
                tables = extract_tables(html_content)

                for table_data in tables:
                    cleaned_table = process_table(table_data)
                    if not cleaned_table:
                        continue
                    
                    # Each cleaned_table has `headers` and `rows`
                    # Example of final_headers: ["Title", "Release Date", "Genre", "Language", "Status", "Category"]
                    # cleaned_table["rows"] might look like [[title, "2025-01-01", "Action", "English", "Active", "Uncategorized"], ...]
                    
                    # 6) Insert each row while checking for duplicates
                    for row in cleaned_table["rows"]:
                        title = row[0]
                        release_date = row[1]
                        
                        # Check for existing record
                        existing = db.query(OriginalContent).filter_by(title=title, release_date=release_date).first()
                        if existing:
                            continue  # Skip duplicates

                        # Otherwise, create a new OriginalContent entry
                        # Adjust indices to match your final_headers
                        # Let's assume your process_table sets columns in this order:
                        # [Title, Release_date, Genre, Language, Status]
                        # and you want to fill your DB model with them:
                        genre = row[2]
                        language = row[3]
                        status = row[4]
                        category = row[5]

                        # Convert release_date to a datetime object
                        parsed_date = None
                        if release_date:
                            try:
                                parsed_date = datetime.strptime(release_date, "%Y-%m-%d")
                            except ValueError:
                                # handle partial or invalid date
                                pass

                        new_entry = OriginalContent(
                            title=title,
                            type=current_type,
                            service=current_service,
                            language=language,
                            release_date=parsed_date,
                            genre=genre,
                            status=status,
                            category=category,
                            source_id=source_id
                        )
                        
                        db.add(new_entry)
                    
                    print(f"Inserted {len(cleaned_table['rows'])} new entries for {current_service} {current_type} content")
            db.commit()

    # 7) Commit all changes
    db.commit()
    db.close()

    print("Database updated successfully!")


if __name__ == "__main__":
    update_database()