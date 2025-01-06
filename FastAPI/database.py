import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://postgres:root@localhost:5433/originalflix"

DATABASE_URL = (
    f"postgresql://rajveersodhi:{os.getenv('POSTGRES_PASSWORD')}"
    "@originalflix.postgres.database.azure.com:5432/postgres?sslmode=require"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
