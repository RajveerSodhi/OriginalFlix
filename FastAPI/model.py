from database import Base
from sqlalchemy import Column, Integer, String, Date

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    language = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    genre = Column(String, nullable=True)
    status = Column(String, nullable=True)