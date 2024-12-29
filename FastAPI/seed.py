from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import NetflixOriginal, DATABASE_URL

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
        existing_entry = db.query(NetflixOriginal).filter_by(title=title).first()
        if not existing_entry:
            db.add(NetflixOriginal(title=title, type="Series", language="English", release_date="2025-1-1"))
    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()