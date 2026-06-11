from sqlalchemy import Column, Integer, String, Text, JSON
from .database import Base

class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String, nullable=False)
    keywords = Column(JSON, nullable=False)
    category = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, nullable=False)
    preferences = Column(Text, nullable=True)
    current_intent = Column(String, nullable=True)