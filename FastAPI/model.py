from database import Base
from sqlalchemy import Column, Integer, String, Date

class OriginalContent(Base):
    __tablename__ = "originalcontent"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    service = Column(String, nullable=False)
    language = Column(String, nullable=True, default="Unknown")
    release_date = Column(Date, nullable=True)
    genre = Column(String, nullable=True, default="Unknown")
    status = Column(String, nullable=True, default="NA")