from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Bookshelf(Base):
    __tablename__ = 'bookshelf'
    __table_args__ = {'schema': 'bookron'}

    book_isbn = Column(String(17), primary_key=True)
    user_email = Column(String(50), primary_key=True)
