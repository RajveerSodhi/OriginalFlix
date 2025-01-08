from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = f"postgresql://{getenv('LOCAL_POSTGRES_ADMIN')}:{getenv('LOCAL_POSTGRES_PASSWORD')}@{getenv('LOCAL_POSTGRES_HOST')}:{getenv('LOCAL_POSTGRES_PORT')}/{getenv('LOCAL_POSTGRES_DB')}"
# DATABASE_URL = (
#     f"postgresql://{getenv('AZURE_POSTGRES_ADMIN')}:{getenv('AZURE_POSTGRES_PASSWORD')}"
#     f"@{getenv('AZURE_POSTGRES_HOST')}:{getenv('AZURE_POSTGRES_PORT')}/{getenv('AZURE_POSTGRES_DB')}?sslmode=require"
# )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
