from sqlalchemy import Column, Integer, String, Text
from app.database.database import Base

class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    status = Column(String)

    results = Column(Text)