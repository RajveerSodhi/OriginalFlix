from database import Base
from sqlalchemy import Column, Integer, String, Date

class NetflixOriginal(Base):
    __tablename__ = "netflix_originals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    language = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    genre = Column(String, nullable=True)