from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'
    __table_args__ = {'schema': 'bookron'}

    isbn = Column(String(17), primary_key=True)
    title = Column(String(256), nullable=False)
    author = Column(String(50), nullable=False)
    publish_year = Column(Integer, nullable=True)
