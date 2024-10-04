from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'bookron'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(500), nullable=False)