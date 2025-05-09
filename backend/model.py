from database import Base
from sqlalchemy import Column, Integer, String, Date

class OriginalContent(Base):
    __tablename__ = "originalcontent"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    service = Column(String, nullable=False)
    release_date = Column(Date, nullable=True, default="2035-01-01")
    genre = Column(String, nullable=True, default="Unknown")
    language = Column(String, nullable=True, default="Unknown")
    status = Column(String, nullable=True, default="NA")
    category = Column(String, nullable=True, default="Uncategorized")
    source_id = Column(Integer, nullable=True, default=0)