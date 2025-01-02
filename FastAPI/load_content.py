from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import DATABASE_URL
from model import OriginalContent

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Seed data: Example Netflix original titles
titles = [
    "Stranger Things",
    "The Witcher",
    "Squid Game",
    "Money Heist",
    "Bridgerton",
    "The Crown",
    "Narcos",
    "Dark",
    "You",
]

def seed_database():
    db = SessionLocal()
    for title in titles:
        existing_entry = db.query(OriginalContent).filter_by(title=title).first()
        if not existing_entry:
            db.add(OriginalContent(title=title, type="Series", language="English", release_date="2025-1-1", genre="Drama", status="Active"))
    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()