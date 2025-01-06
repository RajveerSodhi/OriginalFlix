from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://postgres:root@localhost:5433/originalflix"
DATABASE_URL = (
    "postgresql://rajveersodhi:Postgres!"
    "@originalflix.postgres.database.azure.com:5432/postgres?sslmode=require"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
