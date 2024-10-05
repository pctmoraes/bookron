from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'
    __table_args__ = {'schema': 'bookron'}

    id = Column(Integer, primary_key=True)
    isbn = Column(String(17), nullable=False)
    title = Column(Integer, nullable=False)
    author = Column(String(50), nullable=False)
    publish_year = Column(Integer, nullable=True)
